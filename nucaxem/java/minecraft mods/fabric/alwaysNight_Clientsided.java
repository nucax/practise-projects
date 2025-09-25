// source code btw
package com.yourname.alwaysmidnight;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.minecraft.client.MinecraftClient;

public class AlwaysMidnight implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (client.world != null) {
                // Force the client’s world time every tick
                client.world.setTimeOfDay(18000);
            }
        });
    }
}
