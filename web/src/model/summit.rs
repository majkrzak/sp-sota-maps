use serde::Deserialize;

use super::reference::Reference;

#[derive(Debug, Clone, PartialEq, Eq, Deserialize)]
pub struct Summit {
    #[serde(alias = "summitCode")]
    pub reference: Reference,
    name: String,
}
