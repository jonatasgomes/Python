drop sequence st2_trx_sq;

create sequence st2_trx_sq start with 1 increment by 1 nocache;

drop table st2_trx cascade constraints;

create table st2_trx (
  id number(10) not null,
  algo_id varchar2(30) not null,
  stock_id varchar2(30) not null,
  trx_date date not null,
  type varchar2(1) not null,
  qty number not null,
  price number not null,
  comm number default 0 not null,
  amt number not null,
  balance_entry number not null,
  notes varchar2(128),
  updated_at timestamp(6) with time zone not null,
  updated_by varchar2(128) not null,
  constraint st2_trx_pk primary key (id),
  constraint st2_trx_uq1 unique (algo_id, stock_id, trx_date),
  constraint st2_trx_ck1 check (type in ('B', 'S')),
  constraint st2_trx_ck2 check (qty > 0),
  constraint st2_trx_ck3 check (price > 0),
  constraint st2_trx_ck4 check (comm >= 0),
  constraint st2_trx_ck5 check (amt > 0)
);

comment on table st2_trx is 'Stock Market Transactions';
comment on column st2_trx.id is 'ID';
comment on column st2_trx.algo_id is 'Algorithm ID';
comment on column st2_trx.stock_id is 'Stock ID';
comment on column st2_trx.trx_date is 'Date';
comment on column st2_trx.type is 'Type - (B)uy, (S)ell';
comment on column st2_trx.qty is 'Quantity';
comment on column st2_trx.price is 'Price';
comment on column st2_trx.comm is 'Commission';
comment on column st2_trx.amt is 'Amount';
comment on column st2_trx.balance_entry is 'Balance Entry Amount';
comment on column st2_trx.notes is 'Notes';
comment on column st2_trx.updated_at is 'Last Update Date';
comment on column st2_trx.updated_by is 'Last Update By';

create or replace trigger st2_trx_biu before insert or update on st2_trx for each row
begin
  if inserting then
    if :new.id is null then
      :new.id := st2_trx_sq.nextval;
    end if;
  end if;
  :new.updated_at := systimestamp;
  :new.updated_by := coalesce(sys_context('USERENV', 'OS_USER'), user);
end;
/
