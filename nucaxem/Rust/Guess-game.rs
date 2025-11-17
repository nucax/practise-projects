use rand::Rng;
use std::io;

fn main() {
    let secret = rand::thread_rng().gen_range(1..=10);
    println!("Guess a number 1–10:");

    let mut guess = String::new();
    io::stdin().read_line(&mut guess).unwrap();

    let guess: i32 = guess.trim().parse().unwrap();
    if guess == secret {
        println!("Correct!");
    } else {
        println!("Wrong, the answer was {}", secret);
    }
}
