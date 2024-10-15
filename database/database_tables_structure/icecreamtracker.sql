--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2024-09-12 11:05:48

-- Creating an admin user to test with
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles 
      WHERE rolname = 'admin'
   ) THEN
      CREATE ROLE admin WITH LOGIN PASSWORD 'password';
   END IF;
END
$$;


DROP SCHEMA IF EXISTS tracker CASCADE;;


DROP TABLE IF EXISTS tracker.Customer;
DROP TABLE IF EXISTS tracker.Employee;
DROP TABLE IF EXISTS tracker.Inventory;
DROP TABLE IF EXISTS tracker.Order;
DROP TABLE IF EXISTS tracker.ticket;



SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: tracker; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA tracker;

--
-- TOC entry 4826 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA tracker; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA tracker IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 25042)
-- Name: Customer; Type: TABLE; Schema: tracker; Owner: postgres
--

CREATE TABLE tracker.Customer (
    company character varying NOT NULL,
    password character varying DEFAULT 'password'::character varying NOT NULL,
    status character varying DEFAULT 'ok'::character varying
);



--
-- TOC entry 216 (class 1259 OID 25058)
-- Name: Employee; Type: TABLE; Schema: tracker; Owner: postgres
--

CREATE TABLE tracker.Employee (
    name character varying NOT NULL,
    password character varying DEFAULT 'password'::character varying,
    admin boolean DEFAULT false
);



--
-- TOC entry 218 (class 1259 OID 25068)
-- Name: Inventory; Type: TABLE; Schema: tracker; Owner: postgres
--

CREATE TABLE tracker.Inventory (
    id integer NOT NULL,
    flavor character varying NOT NULL,
    size character varying NOT NULL,
    cost numeric DEFAULT 5.00,
    available integer DEFAULT 0,
    committed integer DEFAULT 0,
    defective integer DEFAULT 0
);



--
-- TOC entry 217 (class 1259 OID 25067)
-- Name: Inventory_id_seq; Type: SEQUENCE; Schema: tracker; Owner: postgres
--

CREATE SEQUENCE tracker."Inventory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- TOC entry 4827 (class 0 OID 0)
-- Dependencies: 217
-- Name: Inventory_id_seq; Type: SEQUENCE OWNED BY; Schema: tracker; Owner: postgres
--

ALTER SEQUENCE tracker."Inventory_id_seq" OWNED BY tracker.Inventory.id;


--
-- TOC entry 219 (class 1259 OID 25080)
-- Name: Order; Type: TABLE; Schema: tracker; Owner: postgres
--

CREATE TABLE tracker.Order (
    id integer NOT NULL,
    company character varying NOT NULL,
    boxes integer DEFAULT 0,
    order_date date DEFAULT '2099-12-31'::date,
    estimated_arrival date,
    arrival date,
    shipping_method character varying,
    shipping_address character varying,
    billing_address character varying,
    shipping_status character varying,
    subtotal_cost numeric,
    shipping_cost numeric,
    total_cost numeric,
    payment_date date
);



--
-- TOC entry 220 (class 1259 OID 25092)
-- Name: ticket; Type: TABLE; Schema: tracker; Owner: postgres
--

CREATE TABLE tracker.ticket (
    id integer NOT NULL,
    source character varying,
    type character varying,
    description character varying,
    status character varying DEFAULT 'open'::character varying,
    report_date date,
    date_detected date,
    date_resolved date,
    resolution character varying
);



--
-- TOC entry 4654 (class 2604 OID 25071)
-- Name: Inventory id; Type: DEFAULT; Schema: tracker; Owner: postgres
--

ALTER TABLE ONLY tracker.Inventory ALTER COLUMN id SET DEFAULT nextval('tracker."Inventory_id_seq"'::regclass);


--
-- TOC entry 4815 (class 0 OID 25042)
-- Dependencies: 215
-- Data for Name: Customer; Type: TABLE DATA; Schema: tracker; Owner: postgres
--

COPY tracker.Customer (company, password, status) FROM stdin;
bk	burger	ok
kfc	chicken	ok
\.


--
-- TOC entry 4816 (class 0 OID 25058)
-- Dependencies: 216
-- Data for Name: Employee; Type: TABLE DATA; Schema: tracker; Owner: postgres
--

COPY tracker.Employee (name, password, admin) FROM stdin;
steve	craft	FALSE
matthew	password	TRUE
\.


--
-- TOC entry 4818 (class 0 OID 25068)
-- Dependencies: 218
-- Data for Name: Inventory; Type: TABLE DATA; Schema: tracker; Owner: postgres
--

COPY tracker.Inventory (id, flavor, size, cost, available, committed, defective) FROM stdin;
1	vanilla	L	4.99	100	0	0
2	chocolate	M	3.99	50	25	25
3	strawberry	S	2.99	25	50	30
\.


--
-- TOC entry 4819 (class 0 OID 25080)
-- Dependencies: 219
-- Data for Name: Order; Type: TABLE DATA; Schema: tracker; Owner: postgres
--

COPY tracker.Order (id, company, boxes, order_date, estimated_arrival, arrival, shipping_method, shipping_address, billing_address, shipping_status, subtotal_cost, shipping_cost, total_cost, payment_date) FROM stdin;
0	kfc	5	2024-09-11	2024-10-30	2099-12-31	shipping	55 First St. San Diego, 91915, CA	55 First St. San Diego, 91915, CA	shipped	4.99	15.99	20.98	2024-09-12
1	bk	3	2024-09-13	2024-09-13	2099-12-31	air	52 Second St. San Diego, 91915, CA	52 Second St. San Diego, 91915, CA	ordered	3.99	8.00	10.99	2024-09-15
\.


--
-- TOC entry 4820 (class 0 OID 25092)
-- Dependencies: 220
-- Data for Name: ticket; Type: TABLE DATA; Schema: tracker; Owner: postgres
--

COPY tracker.ticket (id, source, type, description, status, report_date, date_detected, date_resolved, resolution) FROM stdin;
0	kfc	misc	bogo deal isnt working	open	2024-09-15	2024-09-14	\N	\N
1	steve	inventory	chocolate ice cream spoiled	working on	2024-09-15	2024-09-11	\N	\N
2	bk	shipping	product lost while shipping order	closed	2024-09-15	2024-09-15	2024-09-15	shipping replaced lost items
\.


--
-- TOC entry 4828 (class 0 OID 0)
-- Dependencies: 217
-- Name: Inventory_id_seq; Type: SEQUENCE SET; Schema: tracker; Owner: postgres
--

SELECT pg_catalog.setval('tracker."Inventory_id_seq"', 1, false);


--
-- TOC entry 4663 (class 2606 OID 25050)
-- Name: Customer Customer_pkey; Type: CONSTRAINT; Schema: tracker; Owner: postgres
--

ALTER TABLE ONLY tracker.Customer
    ADD CONSTRAINT "Customer_pkey" PRIMARY KEY (company);


--
-- TOC entry 4665 (class 2606 OID 25066)
-- Name: Employee Employee_pkey; Type: CONSTRAINT; Schema: tracker; Owner: postgres
--

ALTER TABLE ONLY tracker.Employee
    ADD CONSTRAINT "Employee_pkey" PRIMARY KEY (name);


--
-- TOC entry 4667 (class 2606 OID 25079)
-- Name: Inventory Inventory_pkey; Type: CONSTRAINT; Schema: tracker; Owner: postgres
--

ALTER TABLE ONLY tracker.Inventory
    ADD CONSTRAINT "Inventory_pkey" PRIMARY KEY (id);


--
-- TOC entry 4669 (class 2606 OID 25091)
-- Name: Order Order_pkey; Type: CONSTRAINT; Schema: tracker; Owner: postgres
--

ALTER TABLE ONLY tracker.Order
    ADD CONSTRAINT "Order_pkey" PRIMARY KEY (id);


--
-- TOC entry 4671 (class 2606 OID 25099)
-- Name: ticket ticket_pkey; Type: CONSTRAINT; Schema: tracker; Owner: postgres
--

ALTER TABLE ONLY tracker.ticket
    ADD CONSTRAINT ticket_pkey PRIMARY KEY (id);



--give admin access to tables
GRANT USAGE ON SCHEMA tracker TO admin;
ALTER ROLE admin WITH SUPERUSER;



-- Completed on 2024-09-12 11:05:48

--
-- PostgreSQL database dump complete
--