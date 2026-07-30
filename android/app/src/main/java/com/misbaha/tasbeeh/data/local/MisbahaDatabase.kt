package com.misbaha.tasbeeh.data.local

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [DhikrDefinitionEntity::class, CounterSessionEntity::class, DhikrEventEntity::class],
    version = 1,
    exportSchema = true,
)
abstract class MisbahaDatabase : RoomDatabase() {
    abstract fun dhikrDefinitionDao(): DhikrDefinitionDao
    abstract fun counterSessionDao(): CounterSessionDao
    abstract fun dhikrEventDao(): DhikrEventDao
}
