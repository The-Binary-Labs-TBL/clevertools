use serde::Deserialize;
use std::fs;

#[derive(Debug, Deserialize)]
struct Person {
    name: String,
    age: u32,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let data = fs::read_to_string("data/json_io_test_file.json")?;
    
    let person: Person = serde_json::from_str(&data)?;

    println!("{:?}", person);

    Ok(())
}