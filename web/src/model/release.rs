use serde::Deserialize;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Asset {
    pub name: String,
    pub url: String,
    pub browser_download_url: String,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Release {
    pub name: String,
    pub html_url: String,
    pub tag_name: String,
    pub body: String,
    pub assets: Vec<Asset>,
}

impl Release {
    pub fn asset(&self, name: &str) -> Option<&Asset> {
        self.assets.iter().find(|&x| x.name == name)
    }
}

// https://api.github.com/repos/majkrzak/sp-sota-maps/releases/latest
