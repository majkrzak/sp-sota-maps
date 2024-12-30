use std::{fmt::Display, str::FromStr};

use nom::{
    bytes::complete::take,
    character::complete::{alpha0, char},
    combinator::{eof, map, map_parser, map_res, opt},
};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Reference {
    pub association: String,
    pub region: String,
    pub id: u32,
}

impl Reference {
    pub fn full(&self) -> String {
        format!("{}/{}-{:03}", self.association, self.region, self.id)
    }
    pub fn slug(&self) -> String {
        format!("{}{}{:03}", self.association, self.region, self.id)
    }
}

impl Display for Reference {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.full())
    }
}

#[derive(Error, Debug, PartialEq)]
#[error("Can not parse summit reference. Valid vormats are AA/BB-000 and AABB000.")]
pub struct ReferenceParseError(nom::Err<nom::error::Error<String>>);

impl From<nom::Err<nom::error::Error<&str>>> for ReferenceParseError {
    fn from(err: nom::Err<nom::error::Error<&str>>) -> Self {
        Self(err.map_input(|input| input.into()))
    }
}

impl FromStr for Reference {
    type Err = ReferenceParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (s, association) = map(map_parser(take(2u32), alpha0), |x| {
            String::from(x).to_ascii_uppercase()
        })(s)?;

        let (s, _) = opt(char('/'))(s)?;

        let (s, region) = map(map_parser(take(2u32), alpha0), |x| {
            String::from(x).to_ascii_uppercase()
        })(s)?;

        let (s, _) = opt(char('-'))(s)?;

        let (s, id) = map_res(take(3u32), str::parse)(s)?;

        eof(s)?;

        Ok(Reference {
            association,
            region,
            id,
        })
    }
}

#[test]
fn parse_reference() {
    assert_eq!(
        Reference::from_str("SPBZ002"),
        Ok(Reference {
            association: "SP".into(),
            region: "BZ".into(),
            id: 2,
        })
    );
    assert_eq!(
        Reference::from_str("SP/BZ-002"),
        Ok(Reference {
            association: "SP".into(),
            region: "BZ".into(),
            id: 2,
        })
    );
}
