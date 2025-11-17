use image::GenericImageView;
use std::env;

const ASCII_CHARS: &[u8] = b"@%#*+=-:. "; // dark -> light

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: {} <image_path>", args[0]);
        return;
    }

    let img_path = &args[1];
    let img = image::open(img_path).expect("Failed to open image");

    // Resize for terminal width (~80 chars)
    let (width, height) = img.dimensions();
    let aspect_ratio = height as f32 / width as f32;
    let new_width = 80;
    let new_height = (new_width as f32 * aspect_ratio / 2.0) as u32; // divide by 2 for char height

    let img = img.resize_exact(new_width, new_height, image::imageops::FilterType::Nearest);
    let gray = img.to_luma8(); // grayscale

    for y in 0..gray.height() {
        for x in 0..gray.width() {
            let pixel = gray.get_pixel(x, y);
            let brightness = pixel[0] as f32 / 255.0;
            let idx = (brightness * (ASCII_CHARS.len() - 1) as f32).round() as usize;
            print!("{}", ASCII_CHARS[idx] as char);
        }
        println!();
    }
}
