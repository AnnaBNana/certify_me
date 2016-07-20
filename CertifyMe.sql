--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.3
-- Dumped by pg_dump version 9.5.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: attended_classes; Type: TABLE; Schema: public; Owner: apropas
--

CREATE TABLE attended_classes (
    attendee_id integer,
    class_id integer,
    minutes integer NOT NULL
);


ALTER TABLE attended_classes OWNER TO apropas;

--
-- Name: attendees; Type: TABLE; Schema: public; Owner: apropas
--

CREATE TABLE attendees (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    email character varying(150) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone
);


ALTER TABLE attendees OWNER TO apropas;

--
-- Name: attendees_id_seq; Type: SEQUENCE; Schema: public; Owner: apropas
--

CREATE SEQUENCE attendees_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE attendees_id_seq OWNER TO apropas;

--
-- Name: attendees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: apropas
--

ALTER SEQUENCE attendees_id_seq OWNED BY attendees.id;


--
-- Name: businesses; Type: TABLE; Schema: public; Owner: apropas
--

CREATE TABLE businesses (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    street character varying(250),
    city character varying(250) NOT NULL,
    state character varying(2) NOT NULL,
    zip integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    website character varying(250),
    pdf_url character varying(250),
    email character varying(100),
    social_media_1 character varying(150),
    social_media_2 character varying(150),
    social_media_3 character varying(150)
);


ALTER TABLE businesses OWNER TO apropas;

--
-- Name: businesses_id_seq; Type: SEQUENCE; Schema: public; Owner: apropas
--

CREATE SEQUENCE businesses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE businesses_id_seq OWNER TO apropas;

--
-- Name: businesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: apropas
--

ALTER SEQUENCE businesses_id_seq OWNED BY businesses.id;


--
-- Name: class_instructor; Type: TABLE; Schema: public; Owner: apropas
--

CREATE TABLE class_instructor (
    instructor_id integer,
    class_id integer
);


ALTER TABLE class_instructor OWNER TO apropas;

--
-- Name: classes; Type: TABLE; Schema: public; Owner: apropas
--

CREATE TABLE classes (
    id integer NOT NULL,
    name character varying(350) NOT NULL,
    duration integer NOT NULL,
    email_text text,
    date character varying(150) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    race_verbiage text,
    cvpm_verbiage text,
    race_course_num character varying(50),
    business_id integer
);


ALTER TABLE classes OWNER TO apropas;

--
-- Name: classes_id_seq; Type: SEQUENCE; Schema: public; Owner: apropas
--

CREATE SEQUENCE classes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE classes_id_seq OWNER TO apropas;

--
-- Name: classes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: apropas
--

ALTER SEQUENCE classes_id_seq OWNED BY classes.id;


--
-- Name: clients; Type: TABLE; Schema: public; Owner: apropas
--

CREATE TABLE clients (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    title character varying(150),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    business_id integer
);


ALTER TABLE clients OWNER TO apropas;

--
-- Name: clients_id_seq; Type: SEQUENCE; Schema: public; Owner: apropas
--

CREATE SEQUENCE clients_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE clients_id_seq OWNER TO apropas;

--
-- Name: clients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: apropas
--

ALTER SEQUENCE clients_id_seq OWNED BY clients.id;


--
-- Name: instructors; Type: TABLE; Schema: public; Owner: apropas
--

CREATE TABLE instructors (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone
);


ALTER TABLE instructors OWNER TO apropas;

--
-- Name: instructors_id_seq; Type: SEQUENCE; Schema: public; Owner: apropas
--

CREATE SEQUENCE instructors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE instructors_id_seq OWNER TO apropas;

--
-- Name: instructors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: apropas
--

ALTER SEQUENCE instructors_id_seq OWNED BY instructors.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: apropas
--

CREATE TABLE users (
    id integer NOT NULL,
    password character varying(255) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    permission character varying(50) NOT NULL,
    name character varying(50) NOT NULL,
    email character varying(150) NOT NULL,
    business_id integer
);


ALTER TABLE users OWNER TO apropas;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: apropas
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO apropas;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: apropas
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY attendees ALTER COLUMN id SET DEFAULT nextval('attendees_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY businesses ALTER COLUMN id SET DEFAULT nextval('businesses_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY classes ALTER COLUMN id SET DEFAULT nextval('classes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY clients ALTER COLUMN id SET DEFAULT nextval('clients_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY instructors ALTER COLUMN id SET DEFAULT nextval('instructors_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: attended_classes; Type: TABLE DATA; Schema: public; Owner: apropas
--

COPY attended_classes (attendee_id, class_id, minutes) FROM stdin;
\.


--
-- Data for Name: attendees; Type: TABLE DATA; Schema: public; Owner: apropas
--

COPY attendees (id, name, email, created_at, updated_at) FROM stdin;
\.


--
-- Name: attendees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: apropas
--

SELECT pg_catalog.setval('attendees_id_seq', 2819, true);


--
-- Data for Name: businesses; Type: TABLE DATA; Schema: public; Owner: apropas
--

COPY businesses (id, name, street, city, state, zip, created_at, updated_at, website, pdf_url, email, social_media_1, social_media_2, social_media_3) FROM stdin;
24	Tall Oak Enterprises, LLC	26 Flicker Dr.	Greenville	SC	29609	2016-07-12 10:42:52.673224	2016-07-15 16:13:34.354633	www.DrAndyRoark.com	roarktemplate.pdf	drandyroarkacademy@gmail.com		@DrAndyRoark	
25	My Fake Business	87653 Made Up ln.	Fremont	CA	94538	2016-07-18 14:55:53.462986	\N		\N	apropas@gmail.com			
22	Veterinary Training & Consulting	410 Raymondale Drive #26	South Pasadena	CA	91030	2016-06-01 22:30:20.261584	2016-07-19 12:15:43.959825	www.davidlissrvt.com	lisstemplate.pdf	david@davidlissrvt.com	\N	\N	\N
26	Business LLC	878798 some place rd.	Fremont	CA	94538	2016-07-18 15:16:30.407648	2016-07-19 18:11:18.238921		roarktemplate.pdf	apropas@comcast.net			
23	dummy	1234 some street	Chicago	OH	56789	2016-06-11 00:28:04.188177	2016-06-30 12:53:48.87824	www.blah.com	template.pdf	\N	\N	\N	\N
\.


--
-- Name: businesses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: apropas
--

SELECT pg_catalog.setval('businesses_id_seq', 26, true);


--
-- Data for Name: class_instructor; Type: TABLE DATA; Schema: public; Owner: apropas
--

COPY class_instructor (instructor_id, class_id) FROM stdin;
25	15
26	16
27	17
28	17
29	18
\.


--
-- Data for Name: classes; Type: TABLE DATA; Schema: public; Owner: apropas
--

COPY classes (id, name, duration, email_text, date, created_at, updated_at, race_verbiage, cvpm_verbiage, race_course_num, business_id) FROM stdin;
18	Learn to make things	75	Here's your cert, hope you enjoyed the class.  Visit me any time at www.google.com. Please feel free not to contact me.	2016-07-01	2016-07-18 15:19:05.777558	\N	"This program 883-21608 is approved by the AAVSB RACE to offer a total of 1.50 CE Credits (1.50 max) being available to any one veterinarian: and/or 1.50 Veterinary Technician CE Credits (1.50 max). This RACE approval is for the subject matter categorie(s) of: Category Two: Non-Scientific-Clinical using the delivery method(s) of: Interactive-Distance. This approval is valid in jurisdictions which recognize AAVSB RACE; however, participants are responsible for ascertaining each board's CE requirements"		8972-123	26
15	Dental Radiology - What Lies Beneath!	75	email text	2016-04-11	2016-06-20 12:08:43.559935	2016-07-06 22:48:00.761976	race verbiage		883-21608	22
16	Peeling Bananas 101	75	Congrats on learning to peel bananas! You're awesome!  For more info, go to this link: <a href="www.facebook.com">Facebook</a>	2016-07-27	2016-07-05 17:38:03.145421	2016-07-05 17:38:43.172923	something something blah blah		876-346	22
17	Learn to be a cat lady	75	congrats on finishing the class, time to get more cats!	2016-07-01	2016-07-14 20:04:18.729484	\N	something something blah blah	something something blah blah	987-98	24
\.


--
-- Name: classes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: apropas
--

SELECT pg_catalog.setval('classes_id_seq', 18, true);


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: apropas
--

COPY clients (id, name, title, created_at, updated_at, business_id) FROM stdin;
8	new client	CEO of everything	2016-06-11 00:05:48.808634	\N	23
3	David Liss, BA, RVT, VTS (ECC, SAIM), CVPM	President	2016-06-01 22:30:20.266378	2016-07-01 20:17:17.697715	22
11	Dr. Andy Roark	President/CEO	2016-07-12 10:42:52.822542	\N	24
12	Anna Banana	President	2016-07-18 15:13:00.029869	\N	25
14	John Doe	president/ceo	2016-07-18 15:16:30.41808	\N	26
\.


--
-- Name: clients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: apropas
--

SELECT pg_catalog.setval('clients_id_seq', 14, true);


--
-- Data for Name: instructors; Type: TABLE DATA; Schema: public; Owner: apropas
--

COPY instructors (id, name, created_at, updated_at) FROM stdin;
25	Mary L. Berg, BS, LATG, RVT, VTS(Dentistry)	2016-06-20 12:22:25.287359	\N
26	Jamie Holms VTS(bananas)	2016-07-05 17:38:03.361846	\N
27	Cats	2016-07-14 20:04:18.750538	\N
28	Anna Propas	2016-07-14 20:04:18.75292	\N
29	Bob the mystery instructor	2016-07-18 15:19:05.789831	\N
\.


--
-- Name: instructors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: apropas
--

SELECT pg_catalog.setval('instructors_id_seq', 29, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: apropas
--

COPY users (id, password, created_at, updated_at, permission, name, email, business_id) FROM stdin;
25	$2b$12$aE1wTbQ2eqlNfg8a9hC8p.Atp6zEca.Btqc6b3P/cMWzX9Iz9QRa6	2016-06-02 11:08:51.745716	2016-07-17 14:49:58.284547	super-admin	Anna Propas	apropas@gmail.com	23
34	$2b$12$CSw/A0/MBWKDTCzzwODeqee/XQKwLyUmMiKV97CqWY7y3d2uAuHKO	2016-06-07 12:32:44.906829	2016-07-19 12:14:08.629188	user	Bobbie Roberts	bob@bob.com	22
30	$2b$12$TNlMUVK6ZFtaIJ0dqN5ij.gmk/Lgld3XgTnmEKWj9p7SKC8mExg7S	2016-06-07 11:51:57.636074	2016-06-07 20:16:24.989795	admin	David Liss	david@davidlissrvt.com	22
36	$2b$12$qBcNwk6Ln5ZGOC1MsRtTveQao8HNET1fuon/olrrpWmZYxRdHYCuO	2016-07-12 00:29:47.7231	\N	super-admin	Jamie Holms	jholms@gmail.com	23
37	$2b$12$ggwXv8fBKXq3TkZpXtTffeGdB/cIfuxGurNiaf4LQ3WB6ttG0seNa	2016-07-12 10:55:55.26389	2016-07-13 21:26:45.149501	super-admin	John Doe	jdoe@gmail.com	24
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: apropas
--

SELECT pg_catalog.setval('users_id_seq', 37, true);


--
-- Name: attendees_pkey; Type: CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY attendees
    ADD CONSTRAINT attendees_pkey PRIMARY KEY (id);


--
-- Name: businesses_pkey; Type: CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY businesses
    ADD CONSTRAINT businesses_pkey PRIMARY KEY (id);


--
-- Name: classes_pkey; Type: CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY classes
    ADD CONSTRAINT classes_pkey PRIMARY KEY (id);


--
-- Name: clients_name_key; Type: CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY clients
    ADD CONSTRAINT clients_name_key UNIQUE (name);


--
-- Name: clients_pkey; Type: CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- Name: instructors_name_key; Type: CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY instructors
    ADD CONSTRAINT instructors_name_key UNIQUE (name);


--
-- Name: instructors_pkey; Type: CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY instructors
    ADD CONSTRAINT instructors_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: attended_classes_attendee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY attended_classes
    ADD CONSTRAINT attended_classes_attendee_id_fkey FOREIGN KEY (attendee_id) REFERENCES attendees(id);


--
-- Name: attended_classes_class_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY attended_classes
    ADD CONSTRAINT attended_classes_class_id_fkey FOREIGN KEY (class_id) REFERENCES classes(id);


--
-- Name: class_instructor_class_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY class_instructor
    ADD CONSTRAINT class_instructor_class_id_fkey FOREIGN KEY (class_id) REFERENCES classes(id);


--
-- Name: class_instructor_instructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY class_instructor
    ADD CONSTRAINT class_instructor_instructor_id_fkey FOREIGN KEY (instructor_id) REFERENCES instructors(id);


--
-- Name: classes_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY classes
    ADD CONSTRAINT classes_business_id_fkey FOREIGN KEY (business_id) REFERENCES businesses(id);


--
-- Name: clients_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY clients
    ADD CONSTRAINT clients_business_id_fkey FOREIGN KEY (business_id) REFERENCES businesses(id);


--
-- Name: users_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apropas
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_business_id_fkey FOREIGN KEY (business_id) REFERENCES businesses(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: apropas
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM apropas;
GRANT ALL ON SCHEMA public TO apropas;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

