#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum DoorState {
    LockedClosed,
    UnlockedClosed,
    UnlockedOpen,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum DoorError {
    AlreadyUnlocked,
    DoorOpen,
    Locked,
    AlreadyOpen,
}

fn unlock(state: DoorState) -> Result<DoorState, DoorError> {
    match state {
        DoorState::LockedClosed => Ok(DoorState::UnlockedClosed),
        DoorState::UnlockedClosed => Err(DoorError::AlreadyUnlocked),
        DoorState::UnlockedOpen => Err(DoorError::DoorOpen),
    }
}

fn open(state: DoorState) -> Result<DoorState, DoorError> {
    match state {
        DoorState::LockedClosed => Err(DoorError::Locked),
        DoorState::UnlockedClosed => Ok(DoorState::UnlockedOpen),
        DoorState::UnlockedOpen => Err(DoorError::AlreadyOpen),
    }
}

fn unlock_then_open(state: DoorState) -> Result<DoorState, DoorError> {
    let state = unlock(state)?;
    open(state)
}

fn main() {
    let composed = unlock_then_open(DoorState::LockedClosed);
    let reversed_first_step = open(DoorState::LockedClosed);

    assert_eq!(composed, Ok(DoorState::UnlockedOpen));
    assert_eq!(reversed_first_step, Err(DoorError::Locked));

    println!("unlock_then_open(LockedClosed) = {composed:?}");
    println!("open(LockedClosed) = {reversed_first_step:?}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unlock_covers_every_state() {
        assert_eq!(
            unlock(DoorState::LockedClosed),
            Ok(DoorState::UnlockedClosed)
        );
        assert_eq!(
            unlock(DoorState::UnlockedClosed),
            Err(DoorError::AlreadyUnlocked)
        );
        assert_eq!(unlock(DoorState::UnlockedOpen), Err(DoorError::DoorOpen));
    }

    #[test]
    fn open_covers_every_state() {
        assert_eq!(open(DoorState::LockedClosed), Err(DoorError::Locked));
        assert_eq!(open(DoorState::UnlockedClosed), Ok(DoorState::UnlockedOpen));
        assert_eq!(open(DoorState::UnlockedOpen), Err(DoorError::AlreadyOpen));
    }

    #[test]
    fn operation_order_changes_the_result() {
        assert_eq!(
            unlock_then_open(DoorState::LockedClosed),
            Ok(DoorState::UnlockedOpen),
        );
        assert_eq!(open(DoorState::LockedClosed), Err(DoorError::Locked));
    }
}
