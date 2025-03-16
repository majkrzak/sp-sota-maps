use serde::Deserialize;

use super::reference::Reference;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Summit {
    pub reference: Reference,
    pub name: String,
    pub lat: f32,
    pub lon: f32,
    pub alt: f32,
}
