use serde::Deserialize;

use super::reference::Reference;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Summit {
    pub reference: Reference,
    pub name: String,
    pub lat: f32,
    pub lon: f32,
    pub alt: f32,
    pub insights: SummitInsights,
    pub hmap: SummitHmapInfo,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct SummitInsights {
    pub elevation: f32,
    pub distance: f32,
    pub total_area: f32,
    pub polish_area: f32,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct SummitHmapInfo {
    pub symbols: Vec<String>,
    pub reports: Vec<String>,
}
