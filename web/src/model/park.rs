use serde::Deserialize;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Park {
    pub name: String,
    pub pota: String,
    pub wwff: String,
    pub area: f32,
}
