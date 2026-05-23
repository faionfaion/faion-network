// purpose: Minimum-viable filled-in signing config
// consumes: see AGENTS.md Prerequisites
// produces: Android Keystore and Signing config
// depends-on: content/02-output-contract.xml schema
// token-budget-impact: ~400 tokens when filled

import org.gradle.api.tasks.bundling.Jar

plugins {
    id("com.android.application")
    kotlin("android")
}

android {
    namespace = "net.faion.sample"
    compileSdk = 35

    defaultConfig {
        applicationId = "net.faion.sample"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
    }

    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("FAION_KEYSTORE_PATH") ?: "/missing")
            storePassword = System.getenv("FAION_KEYSTORE_PASS") ?: ""
            keyAlias = System.getenv("FAION_KEY_ALIAS") ?: "upload"
            keyPassword = System.getenv("FAION_KEY_PASS") ?: ""
        }
    }

    buildTypes {
        getByName("release") {
            isMinifyEnabled = true
            signingConfig = signingConfigs.getByName("release")
        }
        getByName("debug") {
            // debug uses default per-developer ~/.android/debug.keystore
        }
    }
}
