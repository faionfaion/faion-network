// Rust API Surface Ownership Cheatsheet
// Rule: accept the most-permissive type, return owned when allocating.

use std::path::Path;
use std::io;

// Accept &str, not &String
fn slugify(input: &str) -> String {
    input.to_lowercase().replace(' ', "-")
}

// Accept &[T], not &Vec<T>
fn sum(values: &[i32]) -> i32 {
    values.iter().sum()
}

// Accept impl AsRef<Path> for maximum flexibility
fn read_lines(path: impl AsRef<Path>) -> io::Result<Vec<String>> {
    std::fs::read_to_string(path).map(|s| s.lines().map(String::from).collect())
}

// Return a borrow when slicing into a parameter
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

// Share across threads: Arc, not Rc
use std::sync::Arc;
fn share_across_threads<T: Send + Sync + 'static>(val: T) -> Arc<T> {
    let shared = Arc::new(val);
    std::thread::spawn({
        let shared = Arc::clone(&shared);
        move || { let _ = &*shared; }
    });
    shared
}

// Single-thread shared mutable — Rc<RefCell<T>> last resort
use std::cell::RefCell;
use std::rc::Rc;
fn single_thread_shared_mut() {
    let counter = Rc::new(RefCell::new(0));
    *counter.borrow_mut() += 1;
    println!("{}", counter.borrow());
}
