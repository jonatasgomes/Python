drop sequence st1_main_seq;

create sequence st1_main_seq;

drop table st1_stocks cascade constraints;

create table st1_stocks (
  id number,
  ticker varchar2(30) not null,
  exchange varchar2(128),
  constraint st1_stocks_pk primary key (id),
  constraint st1_stocks_uq1 unique (ticker, exchange)
);

drop table st1_index_stocks cascade constraints;

create table st1_index_stocks (
  index_id number not null,
  stock_id number not null,
  weight number,
  active varchar2(1) default 'Y' not null,
  constraint st1_index_stocks_pk primary key (index_id, stock_id),
  constraint st1_index_stocks_fk1 foreign key (index_id) references st1_stocks (id),
  constraint st1_index_stocks_fk2 foreign key (stock_id) references st1_stocks (id)
);

drop table st1_stock_prices cascade constraints;

create table st1_stock_prices (
  stock_id number not null,
  price_dt date not null,
  timeframe varchar2(3) not null,
  open number,
  low number,
  high number,
  close number,
  volume number,
  constraint st1_stock_prices_pk primary key (stock_id, price_dt, timeframe),
  constraint st1_stock_prices_ck1 check (timeframe in ('1m', '10m', '30m', '1h', '1d', '1wk', '1mo'))
);

begin
  insert into st1_stocks values (st1_main_seq.nextval, 'NDX', 'CBOE');
  insert into st1_stocks values (st1_main_seq.nextval, 'SPX', 'CBOE');
  commit;
end;
/
