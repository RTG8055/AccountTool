CREATE TABLE items
  (
    item_id varchar(100) PRIMARY KEY,
    Name varchar(100),
    Code varchar(100),
    Description varchar(100),
    curr_qty real
  );

CREATE TABLE invoice
  (
    bill_no varchar(100) PRIMARY KEY,
    party_id varchar(100),
    narration varchar(100),
    total_amt real,
    type varchar(100),
    bill_date date
  );

CREATE TABLE invoice_details
  (
    bill_detail_id varchar(100) PRIMARY KEY,
    bill_no varchar(100),
    item_id varchar(100),
    qty real,
    rate real,
    amount real,
    foreign key(bill_no) REFERENCES invoice(bill_no)
  );

CREATE TABLE app_users
  (
    user_id varchar(100) PRIMARY KEY,
    Name varchar(100),
    email varchar(100),
    password varchar(100),
    access_group varchar(50)
  );

CREATE TABLE debtors
  (
    debtor_id varchar(100) PRIMARY KEY,
    name varchar(100),
    address varchar(100),
    balance real
  );

CREATE TABLE creditors
  (
    creditor_id varchar(100) PRIMARY KEY,
    name varchar(100),
    address varchar(100),
    balance real
  );

CREATE TABLE receive
  (
    receive_id varchar(100) PRIMARY KEY,
    item_id varchar(100),
    Qty real,
    receive_date date,
    creditor_id varchar(100),
    vehicle_no varchar(100),
    FOREIGN KEY(item_id) REFERENCES items(item_id),
    FOREIGN KEY(creditor_id) REFERENCES creditors(creditor_id)
  );

CREATE TABLE dispatch
  (
    dispatch_id varchar(100) PRIMARY KEY,
    item_id varchar(100),
    Qty real,
    dispatch_date date,
    debtor_id varchar(100),
    vehicle_no varchar(100),
    FOREIGN KEY(item_id) REFERENCES items(item_id),
    FOREIGN KEY(debtor_id) REFERENCES debtors(debtor_id)
  );


CREATE TABLE receipts
  (
    receipt_no varchar(100),
    receipt_date date,
    party_id varchar(100),
    amount real
  );

CREATE TABLE daily_inventory
  (
    item_id varchar(100),
    Qty real,
    INV_DATE date,
    bill_no varchar(100),
    PRIMARY KEY (item_id, bill_no),
    FOREIGN KEY(item_id) REFERENCES items(item_id),
    FOREIGN KEY(bill_no) REFERENCES invoice(bill_no)
  );

-------------------------LOGIN-------------------------
DROP PROCEDURE IF EXISTS validate_login;
DELIMITER $$
CREATE PROCEDURE validate_login(in e varchar(100), in p varchar(100))
BEGIN
  SELECT * FROM app_users WHERE email = e and password=p;
END
$$
DELIMITER ;

call validate_login('abc@gmail.com','123');
call validate_login('abc@gmail.com','122');
-------------------------ITEM---------------------------
DROP TRIGGER IF EXISTS trigger_items;
DELIMITER $$
CREATE TRIGGER trigger_items
BEFORE INSERT
ON items
FOR EACH ROW
BEGIN
  DECLARE max_item_id varchar(100);

  IF (NEW.item_id = 'xxx') THEN
    SELECT
      MAX(item_id) INTO max_item_id
    FROM
      items;
    IF (max_item_id IS NULL) THEN
      SELECT 'IT00001' INTO max_item_id;
      SET NEW.item_id = max_item_id;
    ELSE
      SET NEW.item_id = CONCAT(SUBSTR(max_item_id, 1, 2), LPAD(SUBSTR(max_item_id, 3) + 1, 5, '0'));
    END IF;
  END IF;
END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS insert_item;
DELIMITER $$
CREATE PROCEDURE insert_item(IN item_name VARCHAR(100), IN description  VARCHAR(100), IN curr_qty REAL)
BEGIN
  IF EXISTS( SELECT item_id FROM items WHERE  name = item_name )
    THEN select 'Not unique';
  ELSE
    INSERT INTO items(item_id, name, description, curr_qty) VALUES ( 'xxx', item_name, description, curr_qty);
  END IF;
END$$
DELIMITER ;

call insert_item('RIL','','100');
call insert_item('MRPL','','100');
---------------------------------------------------------------------

--------------------------------USER---------------------------------

DROP TRIGGER IF EXISTS trigger_users;
DELIMITER $$
CREATE TRIGGER trigger_users
BEFORE INSERT
ON app_users
FOR EACH ROW
BEGIN
  DECLARE max_user_id varchar(100);

  IF (NEW.user_ID = 'xxx') THEN
    SELECT
      MAX(user_id) INTO max_user_id
    FROM
      app_users;
    IF (max_user_id IS NULL) THEN
      SELECT 'U000001' INTO max_user_id;
      SET NEW.user_ID = max_user_id;
    ELSE
      SET NEW.user_ID = CONCAT(SUBSTR(max_user_id, 1,2), LPAD(SUBSTR(max_user_id, 2) + 1, 5, '0'));
    END IF;
  END IF;
END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS insert_user;
DELIMITER $$
CREATE PROCEDURE insert_user(IN user_name VARCHAR(100), IN user_email  VARCHAR(100), IN user_password VARCHAR(100), IN user_access_group VARCHAR(50))
BEGIN
  IF EXISTS( SELECT user_id FROM app_users WHERE  email = user_email)
    THEN select 'Not unique';
  ELSE
    INSERT INTO app_users(user_id, name, email, password, access_group) VALUES ( 'xxx', user_name, user_email, user_password, user_access_group);
  END IF;
END$$
DELIMITER ;

call insert_user('Rahul','abc@gmail.com','123','all_access');
---------------------------------------------------------------------

--------------------------------DEBTOR---------------------------------

DROP TRIGGER IF EXISTS trigger_debtors;
DELIMITER $$
CREATE TRIGGER trigger_debtors
BEFORE INSERT
ON debtors
FOR EACH ROW
BEGIN
  DECLARE max_debtor_id varchar(100);

  IF (NEW.debtor_ID = 'xxx') THEN
    SELECT
      MAX(debtor_id) INTO max_debtor_id
    FROM
      debtors;
    IF (max_debtor_id IS NULL) THEN
      SELECT 'DB00001' INTO max_debtor_id;
      SET NEW.debtor_ID = max_debtor_id;
    ELSE
      SET NEW.debtor_ID = CONCAT(SUBSTR(max_debtor_id, 1,2), LPAD(SUBSTR(max_debtor_id, 3) + 1, 5, '0'));
    END IF;
  END IF;
END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS insert_debtor;
DELIMITER $$
CREATE PROCEDURE insert_debtor(IN debtor_name VARCHAR(100), IN debtor_address VARCHAR(100), IN debtor_balance REAL)
BEGIN
  IF EXISTS( SELECT debtor_id FROM debtors WHERE  name = debtor_name)
    THEN select 'Not unique';
  ELSE
    INSERT INTO debtors(debtor_id, name, address, balance) VALUES ( 'xxx', debtor_name, debtor_address, debtor_balance);
  END IF;
END$$
DELIMITER ;

call insert_debtor('Rahul','HYD',0);
call insert_debtor('Rahul2','HYD',0);
-------------------------------------------------------------------------

--------------------------------CREDITOR---------------------------------

DROP TRIGGER IF EXISTS trigger_creditors;
DELIMITER $$
CREATE TRIGGER trigger_creditors
BEFORE INSERT
ON creditors
FOR EACH ROW
BEGIN
  DECLARE max_creditor_id varchar(100);

  IF (NEW.creditor_ID = 'xxx') THEN
    SELECT
      MAX(creditor_id) INTO max_creditor_id
    FROM
      creditors;
    IF (max_creditor_id IS NULL) THEN
      SELECT 'CR00001' INTO max_creditor_id;
      SET NEW.creditor_ID = max_creditor_id;
    ELSE
      SET NEW.creditor_ID = CONCAT(SUBSTR(max_creditor_id, 1,2), LPAD(SUBSTR(max_creditor_id, 3) + 1, 5, '0'));
    END IF;
  END IF;
END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS insert_creditor;
DELIMITER $$
CREATE PROCEDURE insert_creditor(IN creditor_name VARCHAR(100), IN creditor_address VARCHAR(100), IN creditor_balance REAL)
BEGIN
  IF EXISTS( SELECT creditor_id FROM creditors WHERE  name = creditor_name)
    THEN select 'Not unique';
  ELSE
    INSERT INTO creditors(creditor_id, name, address, balance) VALUES ( 'xxx', creditor_name, creditor_address, creditor_balance);
  END IF;
END$$
DELIMITER ;

call insert_creditor('Yash','HYD',0);
call insert_creditor('YashR','HYD',0);

---------------------------------------------------------------------

--------------------------------DISPATCH---------------------------------

DROP TRIGGER IF EXISTS trigger_dispatchs;
DELIMITER $$
CREATE TRIGGER trigger_dispatchs
BEFORE INSERT
ON dispatch
FOR EACH ROW
BEGIN
  DECLARE max_dispatch_id varchar(100);

  IF (NEW.dispatch_ID = 'xxx') THEN
    SELECT
      MAX(dispatch_id) INTO max_dispatch_id
    FROM
      dispatch;
    IF (max_dispatch_id IS NULL) THEN
      SELECT 'SA00001' INTO max_dispatch_id;
      SET NEW.dispatch_ID = max_dispatch_id;
    ELSE
      SET NEW.dispatch_ID = CONCAT(SUBSTR(max_dispatch_id, 1,2), LPAD(SUBSTR(max_dispatch_id, 3) + 1, 5, '0'));
    END IF;
  END IF;
END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS insert_dispatch;
DELIMITER $$
CREATE PROCEDURE insert_dispatch(IN n_item_id VARCHAR(100), IN n_QTY REAL, n_dispatch_date DATE, n_debtor_id VARCHAR(100), IN n_vehicle_no VARCHAR(100))
BEGIN
    INSERT INTO dispatch(dispatch_id,item_id, qty, dispatch_date, debtor_id, vehicle_no) VALUES ( 'xxx', n_item_id, n_QTY, n_dispatch_date, n_debtor_id, n_vehicle_no);
END$$
DELIMITER ;

call insert_dispatch('IT00001', 100, '2020-02-04', 'DB00001', '');
call insert_dispatch('IT00002', 100, '2020-07-01', 'DB00002', '');

---------------------------------------------------------------------

--------------------------------RECEIVE---------------------------------

DROP TRIGGER IF EXISTS trigger_receives;
DELIMITER $$
CREATE TRIGGER trigger_receives
BEFORE INSERT
ON receive
FOR EACH ROW
BEGIN
  DECLARE max_receive_id varchar(100);

  IF (NEW.receive_ID = 'xxx') THEN
    SELECT
      MAX(receive_id) INTO max_receive_id
    FROM
      receive;
    IF (max_receive_id IS NULL) THEN
      SELECT 'PU00001' INTO max_receive_id;
      SET NEW.receive_ID = max_receive_id;
    ELSE
      SET NEW.receive_ID = CONCAT(SUBSTR(max_receive_id, 1,2), LPAD(SUBSTR(max_receive_id, 3) + 1, 5, '0'));
    END IF;
  END IF;
END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS insert_receive;
DELIMITER $$
CREATE PROCEDURE insert_receive(IN n_item_id VARCHAR(100), IN n_QTY REAL, n_receive_date DATE, n_creditor_id VARCHAR(100), IN n_vehicle_no VARCHAR(100))
BEGIN
    INSERT INTO receive(receive_id,item_id, qty, receive_date, creditor_id, vehicle_no) VALUES ( 'xxx', n_item_id, n_QTY, n_receive_date, n_creditor_id, n_vehicle_no);
END$$
DELIMITER ;

call insert_receive('IT00001', 100, '2020-02-04', 'CR00001', '');
call insert_receive('IT00002', 100, '2020-07-01', 'CR00002', '');

------------------------------------------------------------------------
-- DROP PROCEDURE IF EXISTS get_data;
-- DELIMITER $$
-- CREATE PROCEDURE get_data(IN table_name VARCHAR(100), IN columns VARCHAR(100), IN cond VARCHAR(100), IN extra VARCHAR(100))
-- BEGIN
--   DECLARE final_cond varchar(100);

--   IF (cond = 'blank') THEN
--     SET final_cond = '';
--   ELSE
--     SET final_cond = CONCAT('WHERE ',cond);

--   IF (extra = 'no') THEN
--     SET final_cond = final_cond;
--   ELSE
--     SET final_cond = CONCAT(final_cond, extra);

--   SELECT columns from table_name where final_cond;
-- END$$
-- DELIMITER ;

-- SET @query = CONCAT('SELECT balance INTO FROM ', party_table, ' WHERE ', party_id, '=',New.party_id, 'INTO ',@balance);
--   PREPARE stmt1 FROM @query;
--   EXECUTE stmt1;
--   DEALLOCATE PREPARE stmt1;

-- DROP PROCEDURE IF EXISTS get_single_value;
-- DELIMITER $$
-- CREATE PROCEDURE get_single_value(IN table_name VARCHAR(100), IN columns VARCHAR(100), IN cond_col VARCHAR(100), IN cond_value VARCHAR(100), OUT out_data varchar(100))
-- BEGIN
--   DECLARE final_cond varchar(100);
--   DECLARE query varchar(255);
--   DECLARE stmt1 varchar(255);

--   SET @query = CONCAT('SELECT ',columns, ' FROM ', table_name, ' WHERE ', final_cond);
--   PREPARE stmt1 FROM @query;
--   EXECUTE stmt1;
--   DEALLOCATE PREPARE stmt1;
-- END$$
-- DELIMITER ;

-- call get_single_value("debtors","balance","debtor_id=DB00001","no",@ans);
---
-- SET query = CONCAT('SELECT balance INTO old_bal FROM ? WHERE party_id=', NEW.party_id);
--   PREPARE stmt1 from @query;
--   EXECUTE stmt1 USING @party_table;
--   DEALLOCATE PREPARE stmt1;

--   SET new_bal = old_bal + NEW.total_amt;

--   SET query = CONCAT('UPDATE ? SET balance = ? WHERE party_id = ', NEW.party_id);
--   PREPARE stmt1 from @query;
--   EXECUTE stmt1 USING @party_table, @new_bal;
--   DEALLOCATE PREPARE stmt1;
--------------------------------INVOICE---------------------------------

DROP TRIGGER IF EXISTS trigger_invoices;
DELIMITER $$
CREATE TRIGGER trigger_invoices
BEFORE INSERT
ON invoice
FOR EACH ROW
BEGIN
  DECLARE max_bill_no varchar(100);

  IF (NEW.bill_no = 'xxx') THEN
    SELECT
      MAX(bill_no) INTO max_bill_no
    FROM
      invoice;
    IF (max_bill_no IS NULL) THEN
      SELECT 'B000001' INTO max_bill_no;
      SET NEW.bill_no = max_bill_no;
    ELSE
      SET NEW.bill_no = CONCAT(SUBSTR(max_bill_no, 1,2), LPAD(SUBSTR(max_bill_no, 3) + 1, 5, '0'));
    END IF;
  END IF;
END$$

DELIMITER ;

DROP TRIGGER IF EXISTS trigger_insert_invoice_update_Balance;
DELIMITER $$
CREATE TRIGGER trigger_insert_invoice_update_Balance
AFTER INSERT
ON invoice
FOR EACH ROW
BEGIN
  DECLARE old_bal REAL;
  DECLARE new_bal REAL;

  IF NEW.type ='receipt' THEN
    SELECT balance INTO old_bal FROM debtors WHERE debtor_id = NEW.party_id;
    SET new_bal = old_bal - NEW.total_amt;
    UPDATE debtors SET balance = new_bal WHERE debtor_id = NEW.party_id;
  ELSEIF NEW.type ='sales' THEN
    SELECT balance INTO old_bal FROM debtors WHERE debtor_id = NEW.party_id;
    SET new_bal = old_bal + NEW.total_amt;
    UPDATE debtors SET balance = new_bal WHERE debtor_id = NEW.party_id;
  ELSEIF NEW.type ='purchase' THEN
    SELECT balance INTO old_bal FROM creditors WHERE creditor_id = NEW.party_id;
    SET new_bal = old_bal + NEW.total_amt;
    UPDATE creditors SET balance = new_bal WHERE creditor_id = NEW.party_id;
  ELSEIF NEW.type ='payment' THEN
    SELECT balance INTO old_bal FROM creditors WHERE creditor_id = NEW.party_id;
    SET new_bal = old_bal - NEW.total_amt;
    UPDATE creditors SET balance = new_bal WHERE creditor_id = NEW.party_id;
  ELSEIF NEW.type ='rsales' THEN
    SELECT balance INTO old_bal FROM debtors WHERE debtor_id = NEW.party_id;
    SET new_bal = old_bal - NEW.total_amt;
    UPDATE debtors SET balance = new_bal WHERE debtor_id = NEW.party_id;
  ELSEIF NEW.type ='rpurchase' THEN
    SELECT balance INTO old_bal FROM creditors WHERE creditor_id = NEW.party_id;
    SET new_bal = old_bal - NEW.total_amt;
    UPDATE creditors SET balance = new_bal WHERE creditor_id = NEW.party_id;
  END IF;

END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS insert_invoice;
DELIMITER $$
CREATE PROCEDURE insert_invoice(IN n_party_id VARCHAR(100), n_narration VARCHAR(100), IN n_total_amt REAL, IN n_type varchar(100), n_bill_date DATE)
BEGIN
    INSERT INTO invoice(bill_no,party_id, narration, total_amt, type, bill_date) VALUES ( 'xxx', n_party_id, n_narration, n_total_amt, n_type, n_bill_date);
END$$
DELIMITER ;

call insert_invoice('DB00001', '', '1000', 'receipt', '2020-07-12');
call insert_invoice('DB00002', '', '100', 'sales', '2020-07-22');
call insert_invoice('CR00001', '', '100', 'purchase', '2020-07-22');
call insert_invoice('CR00002', '', '100', 'payment', '2020-07-22');


DROP TRIGGER IF EXISTS trigger_update_invoice_update_Balance;
DELIMITER $$
CREATE TRIGGER trigger_update_invoice_update_Balance
BEFORE UPDATE
ON invoice
FOR EACH ROW
BEGIN
  DECLARE old_bal REAL;
  DECLARE new_bal REAL;

  IF NEW.type ='receipt' THEN
    SELECT balance INTO old_bal FROM debtors WHERE debtor_id = NEW.party_id;
    SET new_bal = old_bal + OLD.total_amt - NEW.total_amt;
    UPDATE debtors SET balance = new_bal WHERE debtor_id = NEW.party_id;
  ELSEIF NEW.type ='sales' THEN
    SELECT balance INTO old_bal FROM debtors WHERE debtor_id = NEW.party_id;
    SET new_bal = old_bal - OLD.total_amt + NEW.total_amt;
    UPDATE debtors SET balance = new_bal WHERE debtor_id = NEW.party_id;
  ELSEIF NEW.type ='purchase' THEN
    SELECT balance INTO old_bal FROM creditors WHERE creditor_id = NEW.party_id;
    SET new_bal = old_bal - OLD.total_amt + NEW.total_amt;
    UPDATE creditors SET balance = new_bal WHERE creditor_id = NEW.party_id;
  ELSEIF NEW.type ='payment' THEN
    SELECT balance INTO old_bal FROM creditors WHERE creditor_id = NEW.party_id;
    SET new_bal = old_bal + OLD.total_amt - NEW.total_amt;
    UPDATE creditors SET balance = new_bal WHERE creditor_id = NEW.party_id;
  ELSEIF NEW.type ='rsales' THEN
    SELECT balance INTO old_bal FROM debtors WHERE debtor_id = NEW.party_id;
    SET new_bal = old_bal + OLD.total_amt - NEW.total_amt;
    UPDATE debtors SET balance = new_bal WHERE debtor_id = NEW.party_id;
  ELSEIF NEW.type ='rpurchase' THEN
    SELECT balance INTO old_bal FROM creditors WHERE creditor_id = NEW.party_id;
    SET new_bal = old_bal + OLD.total_amt - NEW.total_amt;
    UPDATE creditors SET balance = new_bal WHERE creditor_id = NEW.party_id;
  END IF;

END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS update_invoice;
DELIMITER $$
CREATE PROCEDURE update_invoice(IN n_bill_no VARCHAR(100), IN n_party_id VARCHAR(100), n_narration VARCHAR(100), IN n_total_amt REAL, n_bill_date DATE)
BEGIN
    UPDATE invoice set bill_date = n_bill_date, party_id = n_party_id, narration = n_narration, total_amt = n_total_amt where bill_no = n_bill_no;
END$$
DELIMITER ;

call update_invoice('B000005', 'DB00002','','60000', '2020-07-22');
call update_invoice('B000006', 'CR00002','','600', '2020-07-12');
call update_invoice('B000016', 'DB00002','abcd','2411', '2020-07-12');

--------------------------------------------------------------------------------
--------------------------------INVOICE DETAILS---------------------------------


DROP TRIGGER IF EXISTS trigger_invoices_details;
DELIMITER $$
CREATE TRIGGER trigger_invoices_details
BEFORE INSERT
ON invoice_details
FOR EACH ROW
BEGIN
  DECLARE max_bill_detail_id varchar(100);

  IF (NEW.bill_detail_id = 'xxx') THEN
    SELECT
      MAX(bill_detail_id) INTO max_bill_detail_id
    FROM
      invoice_details;
    IF (max_bill_detail_id IS NULL) THEN
      SELECT 'BD00001' INTO max_bill_detail_id;
      SET NEW.bill_detail_id = max_bill_detail_id;
    ELSE
      SET NEW.bill_detail_id = CONCAT(SUBSTR(max_bill_detail_id, 1,2), LPAD(SUBSTR(max_bill_detail_id, 3) + 1, 5, '0'));
    END IF;
  END IF;
END$$

DELIMITER ;


DROP TRIGGER IF EXISTS trigger_insert_invoice_details_update_Quantity;
DELIMITER $$
CREATE TRIGGER trigger_insert_invoice_details_update_Quantity
AFTER INSERT
ON invoice_details
FOR EACH ROW
BEGIN
  DECLARE old_qty REAL;
  DECLARE new_qty REAL;
  DECLARE b_type varchar(100);
  DECLARE b_date date;


  SELECT curr_qty INTO old_qty FROM items WHERE item_id = NEW.ITEM_ID;
  SELECT type INTO b_type FROM invoice WHERE bill_no = NEW.bill_no;
  SELECT bill_date INTO b_date FROM invoice WHERE bill_no = NEW.bill_no;

  IF b_type ='sales' THEN
    SET new_qty = old_qty - NEW.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = NEW.ITEM_ID;
    INSERT INTO daily_inventory(ITEM_ID,qty, inv_date, bill_no) values (NEW.ITEM_ID, -NEW.qty, b_date, NEW.bill_no);
  ELSEIF b_type ='purchase' THEN
    SET new_qty = old_qty + NEW.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = NEW.ITEM_ID;
    INSERT INTO daily_inventory(ITEM_ID,qty, inv_date, bill_no) values (NEW.ITEM_ID, +NEW.qty, b_date, NEW.bill_no);
  ELSEIF b_type ='rsales' THEN
    SET new_qty = old_qty + NEW.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = NEW.ITEM_ID;
    INSERT INTO daily_inventory(ITEM_ID,qty, inv_date, bill_no) values (NEW.ITEM_ID, +NEW.qty, b_date, NEW.bill_no);
  ELSEIF b_type ='rpurchase' THEN
    SET new_qty = old_qty - NEW.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = NEW.ITEM_ID;
    INSERT INTO daily_inventory(ITEM_ID,qty, inv_date, bill_no) values (NEW.ITEM_ID, -NEW.qty, b_date, NEW.bill_no);
  END IF;

END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS insert_invoice_details;
DELIMITER $$
CREATE PROCEDURE insert_invoice_details(IN n_bill_no VARCHAR(100), item_id VARCHAR(100), IN qty REAL, IN rate REAL, amount REAL)
BEGIN
    INSERT INTO invoice_details(bill_detail_id, bill_no, ITEM_ID, qty, rate, amount) VALUES ('xxx', n_bill_no, item_id, qty, rate, amount);
END$$
DELIMITER ;

call insert_invoice_details('B000001', 'IT00001', 1000, 10, 10000);
call insert_invoice_details('B000002', 'IT00001', 100, 10, 1000);
call insert_invoice_details('B000005', 'IT00001', 2000, 10, 1000);
call insert_invoice_details('B000001', 'IT00002', 100, 10, 1000);
call insert_invoice_details('B000002', 'IT00002', 100, 10, 1000);


DROP TRIGGER IF EXISTS trigger_before_update_invoice_details_update_Quantity;
DELIMITER $$
CREATE TRIGGER trigger_before_update_invoice_details_update_Quantity
BEFORE UPDATE
ON invoice_details
FOR EACH ROW
BEGIN
  DECLARE old_qty REAL;
  DECLARE new_qty REAL;
  DECLARE b_type varchar(100);
  DECLARE b_date date;


  SELECT curr_qty INTO old_qty FROM items WHERE item_id = OLD.ITEM_ID;
  SELECT type INTO b_type FROM invoice WHERE bill_no = OLD.bill_no;
  SELECT bill_date INTO b_date FROM invoice WHERE bill_no = OLD.bill_no;

  IF b_type ='sales' THEN
    SET new_qty = old_qty + OLD.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = OLD.ITEM_ID;
    DELETE from daily_inventory WHERE ITEM_ID = OLD.ITEM_ID and inv_date = b_date and bill_no = OLD.bill_no;
  ELSEIF b_type ='purchase' THEN
    SET new_qty = old_qty - OLD.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = OLD.ITEM_ID;
    DELETE from daily_inventory WHERE ITEM_ID = OLD.ITEM_ID and inv_date = b_date and bill_no = OLD.bill_no;
  ELSEIF b_type ='rsales' THEN
    SET new_qty = old_qty - OLD.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = OLD.ITEM_ID;
    DELETE from daily_inventory WHERE ITEM_ID = OLD.ITEM_ID and inv_date = b_date and bill_no = OLD.bill_no;
  ELSEIF b_type ='rpurchase' THEN
    SET new_qty = old_qty + OLD.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = OLD.ITEM_ID;
    DELETE from daily_inventory WHERE ITEM_ID = OLD.ITEM_ID and inv_date = b_date and bill_no = OLD.bill_no;
  END IF;

END$$

DELIMITER ;

DROP TRIGGER IF EXISTS trigger_after_update_invoice_details_update_Quantity;
DELIMITER $$
CREATE TRIGGER trigger_after_update_invoice_details_update_Quantity
AFTER UPDATE
ON invoice_details
FOR EACH ROW
BEGIN
  DECLARE old_qty REAL;
  DECLARE new_qty REAL;
  DECLARE b_type varchar(100);
  DECLARE b_date date;


  SELECT curr_qty INTO old_qty FROM items WHERE item_id = NEW.ITEM_ID;
  SELECT type INTO b_type FROM invoice WHERE bill_no = NEW.bill_no;
  SELECT bill_date INTO b_date FROM invoice WHERE bill_no = NEW.bill_no;

  IF b_type ='sales' THEN
    SET new_qty = old_qty - NEW.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = NEW.ITEM_ID;
    INSERT INTO daily_inventory(ITEM_ID,qty, inv_date, bill_no) values (NEW.ITEM_ID, -NEW.qty, b_date, NEW.bill_no);
  ELSEIF b_type ='purchase' THEN
    SET new_qty = old_qty + NEW.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = NEW.ITEM_ID;
    INSERT INTO daily_inventory(ITEM_ID,qty, inv_date, bill_no) values (NEW.ITEM_ID, +NEW.qty, b_date, NEW.bill_no);
  ELSEIF b_type ='rsales' THEN
    SET new_qty = old_qty + NEW.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = NEW.ITEM_ID;
    INSERT INTO daily_inventory(ITEM_ID,qty, inv_date, bill_no) values (NEW.ITEM_ID, +NEW.qty, b_date, NEW.bill_no);
  ELSEIF b_type ='rpurchase' THEN
    SET new_qty = old_qty - NEW.qty;
    UPDATE items SET curr_qty = new_qty WHERE item_id = NEW.ITEM_ID;
    INSERT INTO daily_inventory(ITEM_ID,qty, inv_date, bill_no) values (NEW.ITEM_ID, -NEW.qty, b_date, NEW.bill_no);
  END IF;

END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS update_invoice_details;
DELIMITER $$
CREATE PROCEDURE update_invoice_details(IN n_bill_detail_id VARCHAR(100), IN n_bill_no VARCHAR(100), n_item_id VARCHAR(100), IN n_qty REAL, IN n_rate REAL, n_amount REAL)
BEGIN
  UPDATE invoice_details set item_id = n_item_id, qty = n_qty, rate = n_rate, amount = n_amount where bill_detail_id = n_bill_detail_id;
END$$
DELIMITER ;

call update_invoice_details('BD00001', 'B000001', 'IT00001', 1000, 11, 11000);
-- call update_invoice_details('B000016', 'IT00001', 'IT00001', 200, 12, 2400);
---------------------------------------------------------------------


select item_id, qty, INV_DATE, name from daily_inventory d, invoice i, creditors c,debtors db where d.bill_no==i.bill_no and i.party_id in (c.creditor_id, db.debtor_id);

select bill_no, d.item_id, Qty, inv_date, items.name as item_name, debtors.name as party_name from daily_inventory d natural join invoice join debtors on invoice.party_id = debtors.debtor_id join items on d.item_id = items.item_id;

select bill_no, d.item_id, Qty, inv_date, items.name as item_name, creditors.name as party_name from daily_inventory d natural join invoice join creditors on invoice.party_id = creditors.creditor_id join items on d.item_id = items.item_id;


select d.item_id, qty, dispatch_date, items.name as item_name, debtors.name as party_name from dispatch d join items on d.item_id = items.item_id join debtors on d.debtor_id = debtors.debtor_id;
select d.item_id, qty, receive_date, items.name as item_name, creditors.name as party_name from receive d join items on d.item_id = items.item_id join creditors on d.creditor_id = creditors.creditor_id;