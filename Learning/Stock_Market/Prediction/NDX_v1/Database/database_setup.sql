set define off;

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

create table st1_log (
  date_time timestamp(6) with time zone not null,
  log clob
);

create or replace package st1_stocks_pkg authid current_user is
  type t_prices is table of st1_stock_prices%rowtype;
  function get_price_alpha(p_ticker varchar2, p_date date) return t_prices pipelined;
  procedure update_prices_job;
end st1_stocks_pkg;
/

create or replace package body st1_stocks_pkg is

  function get_price_alpha(p_ticker varchar2, p_date date) return t_prices pipelined is
    pragma autonomous_transaction;
    l_url varchar2(4000);
    pieces utl_http.html_pieces;
    l_response clob;
    l_json_response json_object_t;
    l_time_series json_object_t;
    l_dates json_key_list;
    l_api_key varchar2(30) := '';
    l_date varchar2(10);
    l_data json_object_t;
    l_open number;
    l_high number;
    l_low number;
    l_close number;
    l_volume number;
    l_prices st1_stock_prices%rowtype;
  begin
    l_url := 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' || p_ticker || '&apikey=' || l_api_key;
    pieces := utl_http.request_pieces(l_url);
    for i in 1 .. pieces.count loop
      l_response := l_response || pieces(i);
    end loop;
    l_json_response := json_object_t.parse(l_response);
    l_time_series := l_json_response.get_object('Time Series (Daily)');
    l_dates := l_time_series.get_keys;
    for i in 1 .. l_dates.count loop
      l_date := l_dates(i);
      l_data := l_time_series.get_object(l_date);
      l_open := l_data.get_number('1. open');
      l_high := l_data.get_number('2. high');
      l_low := l_data.get_number('3. low');
      l_close := l_data.get_number('4. close');
      l_volume := l_data.get_number('5. volume');
      -- l_prices.price_dt := to_date(l_date);
      l_prices.timeframe := '1d';
      l_prices.open := l_open;
      pipe row (l_prices);
    end loop;
    return;
  exception
    when others then
      insert into st1_log values (systimestamp, dbms_utility.format_error_stack);
      commit;
  end get_price_alpha;

  procedure save_stock_prices(p_stock_id number, p_price_dt date, p_timeframe varchar2, p_open number) is
    pragma autonomous_transaction;
  begin
    insert into st1_log values (localtimestamp, p_stock_id || ', ' || p_timeframe || ', ' || p_open);
    commit;
  end save_stock_prices;

  procedure update_prices_job is
    l_prices t_prices;
  begin
    for i in (
      with s as (
        select id, ticker
          from st1_stocks
         where ticker = 'AAPL'
      )        
      select s.id, p.price_dt, p.timeframe, p.open
        from s, get_price_alpha(s.ticker, trunc(sysdate)) p
    ) loop
      save_stock_prices(i.id, i.price_dt, i.timeframe, i.open);
    end loop;
  end update_prices_job;

end st1_stocks_pkg;
/

declare
  l_url varchar2(4000);
  pieces utl_http.html_pieces;
  l_response clob;
  l_json_response json_object_t;
  l_time_series json_object_t;
  l_dates json_key_list;
  l_api_key varchar2(30) := '';
  l_date varchar2(10);
  l_data json_object_t;
  l_open number;
  l_high number;
  l_low number;
  l_close number;
  l_volume number;
begin
  l_url := 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=' || l_api_key;
  pieces := utl_http.request_pieces(l_url);
  for i in 1 .. pieces.count loop
    l_response := l_response || pieces(i);
  end loop;
  l_json_response := json_object_t.parse(l_response);
  insert into st1_log values (systimestamp, l_response); commit;
  l_time_series := l_json_response.get_object('Time Series (Daily)');
  l_dates := l_time_series.get_keys;
  /*for i in 1 .. l_dates.count loop
    l_date := l_dates(i);
    l_data := l_time_series.get_object(l_date);
    l_open := l_data.get_number('1. open');
    l_high := l_data.get_number('2. high');
    l_low := l_data.get_number('3. low');
    l_close := l_data.get_number('4. close');
    l_volume := l_data.get_number('5. volume');
    dbms_output.put_line('Date: ' || l_date || 
                         ', Open: ' || l_open || 
                         ', High: ' || l_high || 
                         ', Low: ' || l_low || 
                         ', Close: ' || l_close || 
                         ', Volume: ' || l_volume);
  end loop;*/
exception
  when others then dbms_output.put_line(dbms_utility.format_error_stack);
end;
/

begin
  insert into st1_stocks values (st1_main_seq.nextval, 'NDX', 'CBOE');
  insert into st1_stocks values (st1_main_seq.nextval, 'SPX', 'CBOE');
  commit;
end;
/
