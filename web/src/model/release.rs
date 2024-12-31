use serde::Deserialize;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Release {
    pub html_url: String,
    pub tag_name: String,
}

// https://api.github.com/repos/majkrzak/sp-sota-maps/releases/latest
