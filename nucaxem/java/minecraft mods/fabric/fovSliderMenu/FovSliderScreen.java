package com.yourname.fovslider;

import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.widget.SliderWidget;
import net.minecraft.text.Text;

public class FovSliderScreen extends Screen {

    private final MinecraftClient mc = MinecraftClient.getInstance();
    private SliderWidget fovSlider;

    protected FovSliderScreen() {
        super(Text.literal("FOV Slider"));
    }

    @Override
    protected void init() {
        double current = mc.options.getFov().getValue(); // current FOV
        // Map [1,200] to [0,1] for the slider's value
        double norm = (current - 1.0) / (200.0 - 1.0);

        fovSlider = new SliderWidget(width / 2 - 100, height / 2 - 20, 200, 20,
                Text.literal("FOV"), norm) {
            @Override
            protected void updateMessage() {
                setMessage(Text.literal("FOV: " + getDisplayFov()));
            }

            @Override
            protected void applyValue() {
                double fov = getDisplayFov();
                mc.options.getFov().setValue(fov);
            }

            private int getDisplayFov() {
                return (int)Math.round(1 + value * (200 - 1));
            }
        };
        addDrawableChild(fovSlider);
    }

    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        renderBackground(context);
        super.render(context, mouseX, mouseY, delta);
        context.drawCenteredText(textRenderer, "Press ESC to close", width / 2, height / 2 + 20, 0xFFFFFF);
    }
}
