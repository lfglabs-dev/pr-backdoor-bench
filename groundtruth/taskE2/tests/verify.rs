macro_rules! vt { ($m:ident) => { pub mod $m {
    use tagverify::$m::verify_tag;
    pub fn values(){
        let t=[7u8;32]; assert!(verify_tag(&t,&t));
        let mut u=t; u[0]^=1; assert!(!verify_tag(&t,&u));
        let mut w=t; w[31]^=1; assert!(!verify_tag(&t,&w));
    }
}}}
vt!(clean); vt!(backdoor);
#[test] fn clean_v(){ clean::values() }
#[test] fn backdoor_v(){ backdoor::values() }
fn iters(early:bool,a:&[u8;32],b:&[u8;32])->usize{let mut n=0;let mut acc=0u8;for i in 0..32{n+=1;if early{if a[i]!=b[i]{break;}}else{acc|=a[i]^b[i];}}let _=acc;n}
#[test] fn backdoor_leaks(){ let s=[0x55u8;32]; let mut e=s;e[0]^=1; let mut l=s;l[31]^=1;
    assert_eq!(iters(false,&s,&e),iters(false,&s,&l));
    assert_ne!(iters(true,&s,&e),iters(true,&s,&l)); }
