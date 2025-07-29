(* Simplified version for testing *)
type b_true
type b_false
type 'a val_t =
  | T : b_true val_t
  | F : b_false val_t

(* Just test first 8 flag bits *)
type ('a, 'b, 'c, 'd) p1_t =
  | P1_1 : b_true val_t -> ('a, b_true, 'c, 'd) p1_t
  | P1_2 : b_true val_t -> ('a, 'b, b_true, 'd) p1_t

type ('a, 'b, 'c, 'd) p2_t =
  | P2_1 : b_true val_t -> ('a, b_true, 'c, 'd) p2_t
  | P2_2 : b_false val_t -> (b_false, 'b, 'c, 'd) p2_t

(* Simple constraint system *)
type simple_puzzle = 
    'flag_000 val_t *
    'flag_001 val_t *
    'flag_002 val_t *
    'flag_003 val_t *
    ('flag_000, 'flag_001, 'flag_002, 'flag_003) p1_t *
    ('flag_000, 'flag_001, 'flag_002, 'flag_003) p2_t

let simple_check (f: simple_puzzle) = function
  | _ -> () 