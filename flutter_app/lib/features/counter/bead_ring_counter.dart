import 'package:flutter/material.dart';

/// The core interaction surface of the whole app: a radial progress ring with a
/// central tap target. Spring-scale press animation, no jarring motion.
class BeadRingCounter extends StatefulWidget {
  const BeadRingCounter({
    super.key,
    required this.currentCount,
    required this.targetCount,
    required this.onTap,
  });

  final int currentCount;
  final int targetCount;
  final VoidCallback onTap;

  @override
  State<BeadRingCounter> createState() => _BeadRingCounterState();
}

class _BeadRingCounterState extends State<BeadRingCounter> with SingleTickerProviderStateMixin {
  late final AnimationController _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 90),
    lowerBound: 0,
    upperBound: 0.04,
  );

  void _handleTap() {
    _controller.forward().then((_) => _controller.reverse());
    widget.onTap();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final progress = widget.targetCount > 0 ? (widget.currentCount / widget.targetCount).clamp(0.0, 1.0) : 0.0;

    return GestureDetector(
      onTap: _handleTap,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          final scale = 1 - _controller.value;
          return Transform.scale(scale: scale, child: child);
        },
        child: Semantics(
          button: true,
          label: '${widget.currentCount} / ${widget.targetCount}',
          child: AspectRatio(
            aspectRatio: 1,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  TweenAnimationBuilder<double>(
                    duration: const Duration(milliseconds: 350),
                    curve: Curves.easeOut,
                    tween: Tween(begin: 0, end: progress),
                    builder: (context, value, _) {
                      return CustomPaint(
                        size: Size.infinite,
                        painter: _RingPainter(
                          progress: value,
                          trackColor: theme.colorScheme.surfaceContainerHighest,
                          progressColor: theme.colorScheme.primary,
                        ),
                      );
                    },
                  ),
                  FractionallySizedBox(
                    widthFactor: 0.62,
                    heightFactor: 0.62,
                    child: DecoratedBox(
                      decoration: BoxDecoration(color: theme.colorScheme.surface, shape: BoxShape.circle),
                      child: Center(
                        child: Text(
                          '${widget.currentCount}',
                          style: theme.textTheme.headlineLarge?.copyWith(fontSize: 48),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _RingPainter extends CustomPainter {
  _RingPainter({required this.progress, required this.trackColor, required this.progressColor});

  final double progress;
  final Color trackColor;
  final Color progressColor;

  @override
  void paint(Canvas canvas, Size size) {
    final strokeWidth = size.shortestSide * 0.07;
    final rect = Offset.zero & size;
    final center = rect.center;
    final radius = (size.shortestSide - strokeWidth) / 2;

    final trackPaint = Paint()
      ..color = trackColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    canvas.drawCircle(center, radius, trackPaint);

    final progressPaint = Paint()
      ..color = progressColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    const startAngle = -1.5707963267948966; // -90deg
    final sweepAngle = 6.283185307179586 * progress; // 2*pi * progress
    canvas.drawArc(Rect.fromCircle(center: center, radius: radius), startAngle, sweepAngle, false, progressPaint);
  }

  @override
  bool shouldRepaint(covariant _RingPainter oldDelegate) =>
      oldDelegate.progress != progress || oldDelegate.progressColor != progressColor;
}
