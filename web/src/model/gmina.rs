use serde::Deserialize;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Gmina {
    pub name: String,
    pub pga: String,
    pub area: f32,
}
