package com.yourname.fovslider;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.option.KeyBinding;
import net.minecraft.client.util.InputUtil;
import org.lwjgl.glfw.GLFW;

public class FovSliderMod implements ClientModInitializer {

    private static KeyBinding openMenuKey;

    @Override
    public void onInitializeClient() {
        // Register the '.' key
        openMenuKey = KeyBindingHelper.registerKeyBinding(new KeyBinding(
                "key.fovslider.openmenu",
                InputUtil.Type.KEYSYM,
                GLFW.GLFW_KEY_PERIOD,
                "key.categories.misc"
        ));

        // Check every client tick
        net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (openMenuKey.wasPressed()) {
                client.execute(() ->
                    client.setScreen(new FovSliderScreen())
                );
            }
        });
    }
}
