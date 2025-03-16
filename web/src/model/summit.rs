use serde::Deserialize;

use super::{gmina::Gmina, park::Park, reference::Reference};

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Summit {
    pub reference: Reference,
    pub name: String,
    pub lat: f32,
    pub lon: f32,
    pub alt: f32,
    pub catalog_lat: f32,
    pub catalog_lon: f32,
    pub catalog_alt: f32,
    pub catalog_alt_diff: f32,
    pub catalog_pos_diff: f32,
    pub hmap_symbols: Vec<String>,
    pub hmap_reports: Vec<String>,
    pub area: f32,
    pub gminas: Vec<Gmina>,
    pub parks: Vec<Park>,
}
