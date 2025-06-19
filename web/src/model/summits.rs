use std::ops::Deref;

use serde::Deserialize;

use super::{reference::Reference, summit::Summit};

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Summits(Vec<Summit>);

impl Deref for Summits {
    type Target = Vec<Summit>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl Summits {
    pub fn get(&self, reference: &Reference) -> Option<Summit> {
        return self.iter().find(|x| x.reference == *reference).cloned();
    }
}
