package com.misbaha.tasbeeh.di

import android.content.Context
import androidx.room.Room
import com.misbaha.tasbeeh.data.local.CounterSessionDao
import com.misbaha.tasbeeh.data.local.DhikrDefinitionDao
import com.misbaha.tasbeeh.data.local.DhikrEventDao
import com.misbaha.tasbeeh.data.local.MisbahaDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): MisbahaDatabase =
        Room.databaseBuilder(context, MisbahaDatabase::class.java, "misbaha.db")
            // Local data is journal/session history — see /docs/09-SECURITY-FRAMEWORK.md §2 for
            // the production SQLCipher-at-rest-encryption requirement layered on top of this.
            .fallbackToDestructiveMigration()
            .build()

    @Provides
    fun provideDhikrDefinitionDao(db: MisbahaDatabase): DhikrDefinitionDao = db.dhikrDefinitionDao()

    @Provides
    fun provideCounterSessionDao(db: MisbahaDatabase): CounterSessionDao = db.counterSessionDao()

    @Provides
    fun provideDhikrEventDao(db: MisbahaDatabase): DhikrEventDao = db.dhikrEventDao()
}
