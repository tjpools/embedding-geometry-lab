use std::mem::{align_of, offset_of, size_of};

#[repr(C)]
#[derive(Clone, Copy, Debug, PartialEq)]
struct TokenRecord {
    identifier: u32,
    weight: f32,
    active: bool,
}

const _: () = assert!(size_of::<TokenRecord>() == 12);
const _: () = assert!(align_of::<TokenRecord>() == 4);
const _: () = assert!(offset_of!(TokenRecord, identifier) == 0);
const _: () = assert!(offset_of!(TokenRecord, weight) == 4);
const _: () = assert!(offset_of!(TokenRecord, active) == 8);

fn weighted_identifier(record: TokenRecord) -> f32 {
    if record.active {
        record.identifier as f32 * record.weight
    } else {
        0.0
    }
}

fn main() {
    let record = TokenRecord {
        identifier: 3,
        weight: 0.5,
        active: true,
    };

    println!("size={}", size_of::<TokenRecord>());
    println!("alignment={}", align_of::<TokenRecord>());
    println!(
        "offsets=identifier:{},weight:{},active:{}",
        offset_of!(TokenRecord, identifier),
        offset_of!(TokenRecord, weight),
        offset_of!(TokenRecord, active)
    );
    println!("weighted_identifier={:.1}", weighted_identifier(record));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn layout_matches_declared_contract() {
        assert_eq!(size_of::<TokenRecord>(), 12);
        assert_eq!(align_of::<TokenRecord>(), 4);
        assert_eq!(offset_of!(TokenRecord, identifier), 0);
        assert_eq!(offset_of!(TokenRecord, weight), 4);
        assert_eq!(offset_of!(TokenRecord, active), 8);
    }

    #[test]
    fn active_record_is_computed() {
        let record = TokenRecord {
            identifier: 3,
            weight: 0.5,
            active: true,
        };
        assert_eq!(weighted_identifier(record), 1.5);
    }

    #[test]
    fn inactive_record_is_zeroed() {
        let record = TokenRecord {
            identifier: 3,
            weight: 0.5,
            active: false,
        };
        assert_eq!(weighted_identifier(record), 0.0);
    }
}