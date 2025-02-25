--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.24
-- Dumped by pg_dump version 9.6.24

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: academic_years; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.academic_years (
    id integer NOT NULL,
    start_date date,
    end_date date,
    active boolean
);


ALTER TABLE public.academic_years OWNER TO postgres;

--
-- Name: academic_years_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.academic_years_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.academic_years_id_seq OWNER TO postgres;

--
-- Name: academic_years_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.academic_years_id_seq OWNED BY public.academic_years.id;


--
-- Name: attendances; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attendances (
    id integer NOT NULL,
    student_id integer,
    staff_id integer,
    schools_grades_sections_id integer,
    is_hourly boolean,
    attendence_date date,
    period character varying,
    time_slot integer,
    is_present_morning boolean,
    is_present_afternoon boolean,
    created_by integer,
    created_on timestamp without time zone,
    updated_by integer,
    updated_on timestamp without time zone
);


ALTER TABLE public.attendances OWNER TO postgres;

--
-- Name: attendances_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.attendances_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attendances_id_seq OWNER TO postgres;

--
-- Name: attendances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.attendances_id_seq OWNED BY public.attendances.id;


--
-- Name: clubs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clubs (
    id integer NOT NULL,
    school_id integer,
    title character varying,
    description character varying,
    status boolean
);


ALTER TABLE public.clubs OWNER TO postgres;

--
-- Name: clubs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clubs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clubs_id_seq OWNER TO postgres;

--
-- Name: clubs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clubs_id_seq OWNED BY public.clubs.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events (
    id integer NOT NULL,
    school_id integer,
    title character varying,
    description character varying,
    date timestamp without time zone
);


ALTER TABLE public.events OWNER TO postgres;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO postgres;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: exam_mark_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam_mark_details (
    id integer NOT NULL,
    exam_mark_id integer,
    evaluation_type character varying(50),
    weightage double precision,
    marks_obtained double precision,
    marks_out_of double precision
);


ALTER TABLE public.exam_mark_details OWNER TO postgres;

--
-- Name: exam_mark_details_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exam_mark_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exam_mark_details_id_seq OWNER TO postgres;

--
-- Name: exam_mark_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exam_mark_details_id_seq OWNED BY public.exam_mark_details.id;


--
-- Name: exam_marks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam_marks (
    id integer NOT NULL,
    term character varying(50),
    student_id integer,
    subject_id integer,
    staff_id integer
);


ALTER TABLE public.exam_marks OWNER TO postgres;

--
-- Name: exam_marks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exam_marks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exam_marks_id_seq OWNER TO postgres;

--
-- Name: exam_marks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exam_marks_id_seq OWNED BY public.exam_marks.id;


--
-- Name: fee_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fee_types (
    id integer NOT NULL,
    school_id integer,
    title character varying,
    status integer
);


ALTER TABLE public.fee_types OWNER TO postgres;

--
-- Name: fee_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fee_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fee_types_id_seq OWNER TO postgres;

--
-- Name: fee_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fee_types_id_seq OWNED BY public.fee_types.id;


--
-- Name: fees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fees (
    id integer NOT NULL,
    fee_type_id integer,
    student_id integer,
    actual_fee integer,
    discount_percentage integer,
    fine_percentage integer,
    paid_amount integer,
    payment_date date
);


ALTER TABLE public.fees OWNER TO postgres;

--
-- Name: fees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fees_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fees_id_seq OWNER TO postgres;

--
-- Name: fees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fees_id_seq OWNED BY public.fees.id;


--
-- Name: grades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grades (
    id integer NOT NULL,
    school_id integer,
    title character varying
);


ALTER TABLE public.grades OWNER TO postgres;

--
-- Name: grades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.grades_id_seq OWNER TO postgres;

--
-- Name: grades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grades_id_seq OWNED BY public.grades.id;


--
-- Name: holidays; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.holidays (
    id integer NOT NULL,
    academic_year_id integer,
    school_id integer,
    title character varying,
    holiday_start_date date,
    holiday_end_date date,
    is_one_day boolean,
    is_active boolean
);


ALTER TABLE public.holidays OWNER TO postgres;

--
-- Name: holidays_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.holidays_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.holidays_id_seq OWNER TO postgres;

--
-- Name: holidays_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.holidays_id_seq OWNED BY public.holidays.id;


--
-- Name: houses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.houses (
    id integer NOT NULL,
    school_id integer,
    title character varying,
    description character varying,
    color character varying,
    status boolean
);


ALTER TABLE public.houses OWNER TO postgres;

--
-- Name: houses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.houses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.houses_id_seq OWNER TO postgres;

--
-- Name: houses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.houses_id_seq OWNED BY public.houses.id;


--
-- Name: modules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.modules (
    id integer NOT NULL,
    module_name character varying,
    menu_name character varying,
    parent_id integer,
    is_active boolean,
    is_visible_in_app boolean,
    module_link character varying(256),
    priority integer
);


ALTER TABLE public.modules OWNER TO postgres;

--
-- Name: modules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.modules_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.modules_id_seq OWNER TO postgres;

--
-- Name: modules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.modules_id_seq OWNED BY public.modules.id;


--
-- Name: offers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.offers (
    id integer NOT NULL,
    subscription_id integer,
    title character varying,
    offer_percentage character varying,
    discount_amount character varying,
    additional_amount character varying,
    launch date,
    expiry date,
    is_school_secific boolean,
    status boolean
);


ALTER TABLE public.offers OWNER TO postgres;

--
-- Name: offers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.offers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.offers_id_seq OWNER TO postgres;

--
-- Name: offers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.offers_id_seq OWNED BY public.offers.id;


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissions (
    id integer NOT NULL,
    permission_name character varying,
    is_active boolean
);


ALTER TABLE public.permissions OWNER TO postgres;

--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_id_seq OWNER TO postgres;

--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    role_name character varying,
    role_type character varying,
    is_active boolean
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: school_fee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_fee (
    id integer NOT NULL,
    fee_type_id integer,
    payment_type integer,
    academic_year_id integer,
    fee_amount integer,
    fee_payment_last_date_with_deduction date,
    discount_percentage integer,
    fee_payment_last_date_without_deduction date,
    fee_payment_last_date_with_fine date,
    fine_percentage integer
);


ALTER TABLE public.school_fee OWNER TO postgres;

--
-- Name: school_fee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.school_fee_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.school_fee_id_seq OWNER TO postgres;

--
-- Name: school_fee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.school_fee_id_seq OWNED BY public.school_fee.id;


--
-- Name: school_student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_student (
    id integer NOT NULL,
    student_id integer,
    house_id integer,
    clubs character varying,
    school_grade_section_id integer,
    academic_year_id integer,
    transport_id integer,
    status boolean,
    roll_number character varying
);


ALTER TABLE public.school_student OWNER TO postgres;

--
-- Name: school_student_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.school_student_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.school_student_id_seq OWNER TO postgres;

--
-- Name: school_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.school_student_id_seq OWNED BY public.school_student.id;


--
-- Name: school_subscription; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_subscription (
    id integer NOT NULL,
    school_id integer,
    subscription_id integer,
    offer_id integer,
    academic_year_id integer,
    no_of_students_subscription character varying,
    subscription_amount character varying,
    payment_status integer,
    payment_date date,
    status boolean,
    subscription_date date,
    expiry_date date,
    title character varying(256)
);


ALTER TABLE public.school_subscription OWNER TO postgres;

--
-- Name: school_subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.school_subscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.school_subscription_id_seq OWNER TO postgres;

--
-- Name: school_subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.school_subscription_id_seq OWNED BY public.school_subscription.id;


--
-- Name: school_subscription_module_role_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_subscription_module_role_permission (
    id integer NOT NULL,
    school_subscription_id integer,
    module_id integer,
    role_id integer,
    permission_id integer
);


ALTER TABLE public.school_subscription_module_role_permission OWNER TO postgres;

--
-- Name: school_subscription_module_role_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.school_subscription_module_role_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.school_subscription_module_role_permission_id_seq OWNER TO postgres;

--
-- Name: school_subscription_module_role_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.school_subscription_module_role_permission_id_seq OWNED BY public.school_subscription_module_role_permission.id;


--
-- Name: schools; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schools (
    id integer NOT NULL,
    code character varying,
    title character varying,
    description character varying,
    address character varying,
    phone character varying,
    syllabus character varying,
    status boolean
);


ALTER TABLE public.schools OWNER TO postgres;

--
-- Name: schools_grades_sections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schools_grades_sections (
    id integer NOT NULL,
    school_id integer,
    grade_id integer,
    section_id integer,
    academic_year_id integer
);


ALTER TABLE public.schools_grades_sections OWNER TO postgres;

--
-- Name: schools_grades_sections_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.schools_grades_sections_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schools_grades_sections_id_seq OWNER TO postgres;

--
-- Name: schools_grades_sections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.schools_grades_sections_id_seq OWNED BY public.schools_grades_sections.id;


--
-- Name: schools_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.schools_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schools_id_seq OWNER TO postgres;

--
-- Name: schools_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.schools_id_seq OWNED BY public.schools.id;


--
-- Name: sections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sections (
    id integer NOT NULL,
    school_id integer,
    title character varying
);


ALTER TABLE public.sections OWNER TO postgres;

--
-- Name: sections_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sections_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sections_id_seq OWNER TO postgres;

--
-- Name: sections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sections_id_seq OWNED BY public.sections.id;


--
-- Name: staff_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff_types (
    id integer NOT NULL,
    title character varying
);


ALTER TABLE public.staff_types OWNER TO postgres;

--
-- Name: staff_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.staff_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.staff_types_id_seq OWNER TO postgres;

--
-- Name: staff_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.staff_types_id_seq OWNED BY public.staff_types.id;


--
-- Name: staffs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staffs (
    id integer NOT NULL,
    school_id integer,
    staff_type_id integer,
    first_name character varying,
    middle_name character varying,
    last_name character varying,
    permanent_address character varying,
    communication_address character varying,
    blood_group character varying,
    qualification character varying,
    is_section_in_charge boolean,
    section_details character varying,
    is_transport_in_charge boolean,
    transport_details character varying,
    joining_date date,
    relieving_date date,
    relieving_comment character varying,
    status boolean
);


ALTER TABLE public.staffs OWNER TO postgres;

--
-- Name: staffs_grades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staffs_grades (
    id integer NOT NULL,
    schools_grades_sections_id integer,
    staff_id integer,
    subject_id integer,
    transport_id integer,
    is_class_in_charge boolean,
    class_in_charge_id integer,
    is_class_in_charge_second boolean,
    class_in_charge_second_id integer,
    is_transport_in_charge boolean
);


ALTER TABLE public.staffs_grades OWNER TO postgres;

--
-- Name: staffs_grades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.staffs_grades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.staffs_grades_id_seq OWNER TO postgres;

--
-- Name: staffs_grades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.staffs_grades_id_seq OWNED BY public.staffs_grades.id;


--
-- Name: staffs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.staffs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.staffs_id_seq OWNER TO postgres;

--
-- Name: staffs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.staffs_id_seq OWNED BY public.staffs.id;


--
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    id integer NOT NULL,
    school_id integer,
    student_code character varying,
    first_name character varying,
    middle_name character varying,
    last_name character varying,
    dob date,
    aadhar_number character varying,
    photo character varying,
    date_of_admission date,
    admission_number character varying,
    identification_mark character varying,
    interests character varying,
    hobbies character varying,
    student_email character varying,
    religion character varying,
    caste character varying,
    permanent_address character varying,
    communication_address character varying,
    mother_name character varying,
    father_name character varying,
    father_qualification character varying,
    mother_qualification character varying,
    father_occupation character varying,
    mother_occupation character varying,
    father_mobile character varying,
    mother_mobile character varying,
    father_email character varying,
    mother_email character varying,
    annual_income character varying,
    blood_group character varying,
    mother_tongue character varying,
    is_single_girl boolean,
    is_minority boolean,
    sibling_status boolean,
    relieving_date date,
    relieving_comment character varying,
    status integer
);


ALTER TABLE public.students OWNER TO postgres;

--
-- Name: students_grades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students_grades (
    id integer NOT NULL,
    student_id integer,
    schools_grades_sections_id integer,
    academic_year_id integer,
    transport_id integer,
    promoted boolean
);


ALTER TABLE public.students_grades OWNER TO postgres;

--
-- Name: students_grades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.students_grades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.students_grades_id_seq OWNER TO postgres;

--
-- Name: students_grades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.students_grades_id_seq OWNED BY public.students_grades.id;


--
-- Name: students_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.students_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.students_id_seq OWNER TO postgres;

--
-- Name: students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.students_id_seq OWNED BY public.students.id;


--
-- Name: subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subjects (
    id integer NOT NULL,
    school_id integer,
    title character varying
);


ALTER TABLE public.subjects OWNER TO postgres;

--
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subjects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_id_seq OWNER TO postgres;

--
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- Name: subscription_invoice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscription_invoice (
    id integer NOT NULL,
    school_subscription_id integer,
    invoice_code character varying,
    invoice_file_path character varying,
    invoice_date date
);


ALTER TABLE public.subscription_invoice OWNER TO postgres;

--
-- Name: subscription_invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_invoice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscription_invoice_id_seq OWNER TO postgres;

--
-- Name: subscription_invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscription_invoice_id_seq OWNED BY public.subscription_invoice.id;


--
-- Name: subscriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscriptions (
    id integer NOT NULL,
    title character varying,
    description character varying,
    amount_per_student character varying,
    min_student_count character varying,
    launch date,
    expiry date,
    type character varying,
    status boolean
);


ALTER TABLE public.subscriptions OWNER TO postgres;

--
-- Name: subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscriptions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscriptions_id_seq OWNER TO postgres;

--
-- Name: subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscriptions_id_seq OWNED BY public.subscriptions.id;


--
-- Name: time_table_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.time_table_details (
    id integer NOT NULL,
    time_table_id integer,
    day_name character varying,
    order_number integer,
    time_slot character varying,
    subject_id integer,
    staff_id integer
);


ALTER TABLE public.time_table_details OWNER TO postgres;

--
-- Name: time_table_details_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.time_table_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.time_table_details_id_seq OWNER TO postgres;

--
-- Name: time_table_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.time_table_details_id_seq OWNED BY public.time_table_details.id;


--
-- Name: time_tables; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.time_tables (
    id integer NOT NULL,
    school_id integer,
    academic_year_id integer,
    schools_grades_sections_id integer
);


ALTER TABLE public.time_tables OWNER TO postgres;

--
-- Name: time_tables_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.time_tables_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.time_tables_id_seq OWNER TO postgres;

--
-- Name: time_tables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.time_tables_id_seq OWNED BY public.time_tables.id;


--
-- Name: transports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transports (
    id integer NOT NULL,
    school_id integer,
    driver_id integer,
    driver_code character varying,
    vehicle_number character varying,
    route_number character varying,
    route_name character varying,
    vehicle_gps_device_id character varying,
    vehicle_tracking_url character varying,
    in_charge_id integer
);


ALTER TABLE public.transports OWNER TO postgres;

--
-- Name: transports_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transports_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transports_id_seq OWNER TO postgres;

--
-- Name: transports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transports_id_seq OWNED BY public.transports.id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_roles_id_seq OWNER TO postgres;

--
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    staff_id integer,
    student_id integer,
    username character varying,
    password character varying,
    is_active boolean
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: academic_years id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.academic_years ALTER COLUMN id SET DEFAULT nextval('public.academic_years_id_seq'::regclass);


--
-- Name: attendances id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendances ALTER COLUMN id SET DEFAULT nextval('public.attendances_id_seq'::regclass);


--
-- Name: clubs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clubs ALTER COLUMN id SET DEFAULT nextval('public.clubs_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: exam_mark_details id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_mark_details ALTER COLUMN id SET DEFAULT nextval('public.exam_mark_details_id_seq'::regclass);


--
-- Name: exam_marks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_marks ALTER COLUMN id SET DEFAULT nextval('public.exam_marks_id_seq'::regclass);


--
-- Name: fee_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fee_types ALTER COLUMN id SET DEFAULT nextval('public.fee_types_id_seq'::regclass);


--
-- Name: fees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fees ALTER COLUMN id SET DEFAULT nextval('public.fees_id_seq'::regclass);


--
-- Name: grades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades ALTER COLUMN id SET DEFAULT nextval('public.grades_id_seq'::regclass);


--
-- Name: holidays id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holidays ALTER COLUMN id SET DEFAULT nextval('public.holidays_id_seq'::regclass);


--
-- Name: houses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.houses ALTER COLUMN id SET DEFAULT nextval('public.houses_id_seq'::regclass);


--
-- Name: modules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules ALTER COLUMN id SET DEFAULT nextval('public.modules_id_seq'::regclass);


--
-- Name: offers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.offers ALTER COLUMN id SET DEFAULT nextval('public.offers_id_seq'::regclass);


--
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: school_fee id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_fee ALTER COLUMN id SET DEFAULT nextval('public.school_fee_id_seq'::regclass);


--
-- Name: school_student id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_student ALTER COLUMN id SET DEFAULT nextval('public.school_student_id_seq'::regclass);


--
-- Name: school_subscription id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription ALTER COLUMN id SET DEFAULT nextval('public.school_subscription_id_seq'::regclass);


--
-- Name: school_subscription_module_role_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription_module_role_permission ALTER COLUMN id SET DEFAULT nextval('public.school_subscription_module_role_permission_id_seq'::regclass);


--
-- Name: schools id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools ALTER COLUMN id SET DEFAULT nextval('public.schools_id_seq'::regclass);


--
-- Name: schools_grades_sections id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools_grades_sections ALTER COLUMN id SET DEFAULT nextval('public.schools_grades_sections_id_seq'::regclass);


--
-- Name: sections id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sections ALTER COLUMN id SET DEFAULT nextval('public.sections_id_seq'::regclass);


--
-- Name: staff_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff_types ALTER COLUMN id SET DEFAULT nextval('public.staff_types_id_seq'::regclass);


--
-- Name: staffs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs ALTER COLUMN id SET DEFAULT nextval('public.staffs_id_seq'::regclass);


--
-- Name: staffs_grades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs_grades ALTER COLUMN id SET DEFAULT nextval('public.staffs_grades_id_seq'::regclass);


--
-- Name: students id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students ALTER COLUMN id SET DEFAULT nextval('public.students_id_seq'::regclass);


--
-- Name: students_grades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students_grades ALTER COLUMN id SET DEFAULT nextval('public.students_grades_id_seq'::regclass);


--
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq'::regclass);


--
-- Name: subscription_invoice id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_invoice ALTER COLUMN id SET DEFAULT nextval('public.subscription_invoice_id_seq'::regclass);


--
-- Name: subscriptions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions ALTER COLUMN id SET DEFAULT nextval('public.subscriptions_id_seq'::regclass);


--
-- Name: time_table_details id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_table_details ALTER COLUMN id SET DEFAULT nextval('public.time_table_details_id_seq'::regclass);


--
-- Name: time_tables id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_tables ALTER COLUMN id SET DEFAULT nextval('public.time_tables_id_seq'::regclass);


--
-- Name: transports id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transports ALTER COLUMN id SET DEFAULT nextval('public.transports_id_seq'::regclass);


--
-- Name: user_roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: academic_years; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.academic_years (id, start_date, end_date, active) FROM stdin;
4	2000-04-01	2001-05-30	f
1	2024-04-01	2025-03-31	t
\.


--
-- Name: academic_years_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.academic_years_id_seq', 4, true);


--
-- Data for Name: attendances; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.attendances (id, student_id, staff_id, schools_grades_sections_id, is_hourly, attendence_date, period, time_slot, is_present_morning, is_present_afternoon, created_by, created_on, updated_by, updated_on) FROM stdin;
12	5	1	1	f	2025-01-27	\N	\N	t	t	1	2025-01-28 20:32:38.658247	\N	\N
10	5	1	1	f	2025-01-28	\N	\N	f	f	1	2025-01-28 20:31:16.099636	1	2025-01-29 23:47:02.446627
14	5	1	1	f	2025-01-29	\N	\N	t	t	1	2025-01-29 23:46:58.403507	1	2025-01-29 23:47:09.799395
17	6	1	1	f	2025-02-03	\N	\N	t	f	1	2025-02-03 00:07:06.976747	\N	\N
16	5	1	1	f	2025-02-05	\N	\N	f	f	1	2025-02-03 00:07:06.969727	\N	\N
15	3	1	1	f	2025-02-04	\N	\N	t	f	1	2025-02-03 00:07:06.909338	\N	\N
13	3	1	1	f	2025-01-29	\N	\N	f	f	1	2025-01-29 23:46:58.398444	1	2025-01-29 23:47:09.797397
11	3	1	1	f	2025-02-09	\N	\N	t	t	1	2025-01-28 20:32:38.645175	\N	\N
9	3	1	1	f	2025-02-12	\N	\N	f	t	1	2025-01-28 20:31:16.099636	1	2025-01-29 23:47:02.444615
\.


--
-- Name: attendances_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.attendances_id_seq', 17, true);


--
-- Data for Name: clubs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clubs (id, school_id, title, description, status) FROM stdin;
1	1	Red	qAADSAD	t
7	1	4	    4         	f
8	1	5	  5           	f
9	1	6	 6            	f
10	1	7	7             	f
11	1	8	 8            	f
12	1	9	            0 	f
13	1	10	 10            	f
14	1	11	  11           	f
\.


--
-- Name: clubs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clubs_id_seq', 14, true);


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events (id, school_id, title, description, date) FROM stdin;
1	1	Even 1	test	2025-02-15 20:30:00
3	2	Test school 2	test	2025-02-20 23:45:00
4	1	Even 2	test	2025-02-15 20:30:00
12	1	Events333	test	2025-02-10 13:58:00
13	1	444	4444	2025-02-10 22:03:00
14	1	777777777	\N	2025-02-10 22:13:00
15	1	1112233	test	2025-02-28 22:24:00
16	1	Exam	test	2025-02-12 23:41:00
\.


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_id_seq', 16, true);


--
-- Data for Name: exam_mark_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam_mark_details (id, exam_mark_id, evaluation_type, weightage, marks_obtained, marks_out_of) FROM stdin;
15	13	\N	20	99	100
13	11	\N	20	290	300
14	12	\N	20	180	300
17	15	\N	20	98	100
16	14	\N	20	77	100
18	16	\N	1	24	25
19	17	\N	1	20	25
11	9	\N	10	80.5	100
12	10	\N	10	90	100
20	20	\N	10	60	100
\.


--
-- Name: exam_mark_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exam_mark_details_id_seq', 20, true);


--
-- Data for Name: exam_marks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam_marks (id, term, student_id, subject_id, staff_id) FROM stdin;
9	First	3	1	1
10	First	5	1	1
11	Second	3	1	1
12	Second	5	1	1
13	Third	4	1	1
14	First	3	2	1
15	First	5	2	1
16	Second	5	2	1
17	Second	3	2	1
20	First	6	1	25
\.


--
-- Name: exam_marks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exam_marks_id_seq', 20, true);


--
-- Data for Name: fee_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fee_types (id, school_id, title, status) FROM stdin;
\.


--
-- Name: fee_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fee_types_id_seq', 1, false);


--
-- Data for Name: fees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fees (id, fee_type_id, student_id, actual_fee, discount_percentage, fine_percentage, paid_amount, payment_date) FROM stdin;
\.


--
-- Name: fees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fees_id_seq', 1, false);


--
-- Data for Name: grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.grades (id, school_id, title) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
\.


--
-- Name: grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.grades_id_seq', 7, true);


--
-- Data for Name: holidays; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.holidays (id, academic_year_id, school_id, title, holiday_start_date, holiday_end_date, is_one_day, is_active) FROM stdin;
\.


--
-- Name: holidays_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.holidays_id_seq', 1, false);


--
-- Data for Name: houses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.houses (id, school_id, title, description, color, status) FROM stdin;
1	1	Red	Test1	Red	t
2	1	raman	SEWFREGREGG	Green	t
\.


--
-- Name: houses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.houses_id_seq', 2, true);


--
-- Data for Name: modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modules (id, module_name, menu_name, parent_id, is_active, is_visible_in_app, module_link, priority) FROM stdin;
7	Schools	Schools	\N	t	f	schools/list	1
20	School Subscriptions	School Subscriptions	\N	t	f	school_subscriptions/list	3
3	Subscriptions	Subscriptions	\N	t	t	subscriptions/list	2
18	Modules	Modules	\N	t	f	modules/list	5
19	Module Config	Module Config	\N	t	f	ssmrp/list	6
23	Roles	Roles	\N	t	f	roles/list	7
2	Users	Users	\N	t	f	users/list	8
24	Permissions	Permissions	\N	t	f	permissions/list	9
5	Students	Students	\N	t	t	students/list	10
6	Offers	Offers	\N	t	f	offers/list	4
1	Staffs	Staffs	\N	t	t	staffs/list	12
11	Staff Assignment	Staff Assignment	\N	t	f	staff_assignment/list	13
22	Staff Types	Staff Types	\N	t	f	staff_types/list	11
12	Exams	Exams	\N	t	f	exam-marks	16
14	Subjects	Subjects	\N	t	f	subjects/list	15
15	Transports	Transports	\N	t	f	transports/list	17
16	Grades	Grades	\N	t	f	grades/list	18
17	Sections	Sections	\N	t	f	sections/list	19
21	Houses	Houses	\N	t	f	houses/list	20
4	Clubs	Clubs	\N	t	t	clubs/list	21
25	Timetable	Timetable	\N	t	f	timetable-manage	22
13	Attendances	Attendances	\N	t	f	attendances	14
26	Grade and Section Config	Grade and Section Config	\N	t	f	schools-grades-sections/list	7
\.


--
-- Name: modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.modules_id_seq', 26, true);


--
-- Data for Name: offers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.offers (id, subscription_id, title, offer_percentage, discount_amount, additional_amount, launch, expiry, is_school_secific, status) FROM stdin;
1	1	Offer	50	100	20	2024-11-24	2024-11-30	t	t
2	1	offer2	120	1	2	2024-11-22	2024-11-24	t	t
\.


--
-- Name: offers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.offers_id_seq', 4, true);


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissions (id, permission_name, is_active) FROM stdin;
2	Modify	t
3	Delete	t
6	View	t
1	Create	t
7	Create	f
\.


--
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permissions_id_seq', 8, true);


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, role_name, role_type, is_active) FROM stdin;
2	Student	student	t
3	superadmin	superadmin	t
1	admin	admin	t
4	Student	superadmin	t
\.


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 4, true);


--
-- Data for Name: school_fee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.school_fee (id, fee_type_id, payment_type, academic_year_id, fee_amount, fee_payment_last_date_with_deduction, discount_percentage, fee_payment_last_date_without_deduction, fee_payment_last_date_with_fine, fine_percentage) FROM stdin;
\.


--
-- Name: school_fee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_fee_id_seq', 1, false);


--
-- Data for Name: school_student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.school_student (id, student_id, house_id, clubs, school_grade_section_id, academic_year_id, transport_id, status, roll_number) FROM stdin;
2	4	1	tets	2	1	1	t	1
4	6	1	tets	1	1	1	t	3
3	5	1	Raman	1	4	1	t	2
1	3	1	tets	1	1	1	t	1
\.


--
-- Name: school_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_student_id_seq', 4, true);


--
-- Data for Name: school_subscription; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.school_subscription (id, school_id, subscription_id, offer_id, academic_year_id, no_of_students_subscription, subscription_amount, payment_status, payment_date, status, subscription_date, expiry_date, title) FROM stdin;
2	2	1	1	1	120	120	2	2024-11-26	t	2024-11-01	2024-11-26	S2 Basic
4	1	7	\N	1	12	12	1	2024-11-27	t	2024-11-20	2024-11-29	School 1 Platinum
3	1	1	\N	1	1222	122	2	2024-11-01	f	2024-11-20	2024-11-27	None
\.


--
-- Name: school_subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_subscription_id_seq', 4, true);


--
-- Data for Name: school_subscription_module_role_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.school_subscription_module_role_permission (id, school_subscription_id, module_id, role_id, permission_id) FROM stdin;
4	4	4	2	1
5	2	1	1	1
1	4	1	1	6
6	4	1	2	1
7	4	5	3	1
8	4	6	3	1
9	4	11	3	2
10	2	1	2	2
2	4	3	3	1
11	4	12	3	2
12	4	12	1	2
13	4	13	3	2
14	4	14	3	2
15	4	15	3	2
16	4	16	3	2
17	4	17	3	2
18	4	18	3	2
19	4	19	3	2
20	4	20	3	2
21	4	21	3	2
22	4	22	3	2
23	4	2	3	2
24	4	23	3	2
25	4	24	3	2
26	4	7	3	2
27	4	25	3	2
28	4	26	3	2
\.


--
-- Name: school_subscription_module_role_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_subscription_module_role_permission_id_seq', 28, true);


--
-- Data for Name: schools; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.schools (id, code, title, description, address, phone, syllabus, status) FROM stdin;
1	CODE1	SCHOOL 1	DESC 1	ADDRESS1	9947006717	STATE	t
2	S2	S2	NAASD	ASD	123123	12312	t
\.


--
-- Data for Name: schools_grades_sections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.schools_grades_sections (id, school_id, grade_id, section_id, academic_year_id) FROM stdin;
1	1	1	1	1
2	1	1	2	4
3	2	1	1	1
\.


--
-- Name: schools_grades_sections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.schools_grades_sections_id_seq', 3, true);


--
-- Name: schools_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.schools_id_seq', 3, true);


--
-- Data for Name: sections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sections (id, school_id, title) FROM stdin;
1	1	A
2	1	B
\.


--
-- Name: sections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sections_id_seq', 3, true);


--
-- Data for Name: staff_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staff_types (id, title) FROM stdin;
1	Teacher
6	Clerk
7	HOD
8	clerk
9	HM
\.


--
-- Name: staff_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staff_types_id_seq', 9, true);


--
-- Data for Name: staffs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staffs (id, school_id, staff_type_id, first_name, middle_name, last_name, permanent_address, communication_address, blood_group, qualification, is_section_in_charge, section_details, is_transport_in_charge, transport_details, joining_date, relieving_date, relieving_comment, status) FROM stdin;
3	2	1	AMMU		SANITH	EC Nilayam	CHENGALTHADAM	O+VE	Msc	t	AFDF	t	SDF	2024-11-15	2024-11-21	SFSDF	t
5	1	1	Ishani	Sanith	E	EC NILAYAM, CHENGALTHADAM	PAYANGADI, KANNUR	O+VE	Msc	t	TEST	t	TEST	2024-12-04	2024-12-05	DASD	t
1	1	6	Sanith	E	E	EC NILAYAM, CHENGALTHADAM	PAYANGADI, KANNUR	A+VE	Msc	t	TEST1	t	DASD	2024-11-26	2024-11-28	ASDSAD	t
2	1	1	PRIYANARAYANAN	P	P	EC Nilayam	CHENGALTHADAM	A+VE	MCA	t	ASD	t	ASD	2024-11-15	2024-11-22	ASD	t
4	1	7	Mr. Jacob	P	Varghese	EC Nilayam\r\nCHENGALTHADAM	EC Nilayam\r\nCHENGALTHADAM	A+VE	B-Tech	t	test	t	test	2024-11-01	2024-11-29		t
6	1	1	Ammu	I	Sanith	test	test	0+	mca	t	A	t	A	2025-02-12	2025-02-14	asd	t
\.


--
-- Data for Name: staffs_grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staffs_grades (id, schools_grades_sections_id, staff_id, subject_id, transport_id, is_class_in_charge, class_in_charge_id, is_class_in_charge_second, class_in_charge_second_id, is_transport_in_charge) FROM stdin;
1	1	5	1	1	t	2	t	1	t
\.


--
-- Name: staffs_grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staffs_grades_id_seq', 2, true);


--
-- Name: staffs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staffs_id_seq', 6, true);


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students (id, school_id, student_code, first_name, middle_name, last_name, dob, aadhar_number, photo, date_of_admission, admission_number, identification_mark, interests, hobbies, student_email, religion, caste, permanent_address, communication_address, mother_name, father_name, father_qualification, mother_qualification, father_occupation, mother_occupation, father_mobile, mother_mobile, father_email, mother_email, annual_income, blood_group, mother_tongue, is_single_girl, is_minority, sibling_status, relieving_date, relieving_comment, status) FROM stdin;
6	1	S456	Remya	N	N	2025-02-02	123456	Schoople_Website_1.png	2025-02-01	123	ASD	ASD	ASD	remya@gmail.com	\N	qwe	EC Nilayam	CHENGALTHADAM	AD	SANITH	a	s	d	f	09961094941	09961094941	sanith.e@gmail.com	TEST@TEST11	12321	A+VE	M	f	f	f	\N	\N	1
5	1	TESTCODE1	Ishani	Sanith	E	2015-05-22	AADHARNO987	\N	2024-12-01	8141	ASD	TEST INT	HOBBY	ishanisanith@gmail.com	\N	test	EC NILAYAM, CHENGALTHADAM	PAYANGADI, KANNUR	PRIYA	SANITH	MSC	MCA	SOFTWARE ENGINEER	SOFTWARE ENGINEER	9947006717	9961094941	sanith.e@gmail.com	priyaa.np@gmail.com	5454	O+VE	Malayalam	t	t	t	\N	\N	1
4	1	S456	PRIYANARAYANAN	P	P	2024-12-06	123456	\N	2024-12-04	123	ASD	ASD	ASD	TEST@TEST	ASD	qwe	EC Nilayam	CHENGALTHADAM	AD	ASD	a	s	d	f	09961094941	09947006717	TEST@TEST	TEST@TEST11	12321	A+VE	M	t	t	t	\N	\N	1
3	1	SCODE	Sanith	P	E	2024-12-01	123456	PRIYA_1.jpg	2024-12-05	123	ASD	ASD	ASD	TEST@TEST	\N	qwe	EC NILAYAM, CHENGALTHADAM	PAYANGADI, KANNUR	AD	ASD	a	s	d	f	09947006717	09947006717	TEST@TEST	TEST@TEST11	12321	A+VE	M	t	t	t	\N	\N	1
\.


--
-- Data for Name: students_grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students_grades (id, student_id, schools_grades_sections_id, academic_year_id, transport_id, promoted) FROM stdin;
\.


--
-- Name: students_grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.students_grades_id_seq', 1, false);


--
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.students_id_seq', 6, true);


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subjects (id, school_id, title) FROM stdin;
1	1	English
2	1	Maths
\.


--
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subjects_id_seq', 2, true);


--
-- Data for Name: subscription_invoice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscription_invoice (id, school_subscription_id, invoice_code, invoice_file_path, invoice_date) FROM stdin;
\.


--
-- Name: subscription_invoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscription_invoice_id_seq', 1, false);


--
-- Data for Name: subscriptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscriptions (id, title, description, amount_per_student, min_student_count, launch, expiry, type, status) FROM stdin;
7	Platinum	Plat desc	100	15	2024-11-23	2024-11-30	Prime	t
1	Basic	description1	150	300	2024-11-24	2024-11-30	Test	t
8	Standard	test 111 	12	12	2024-12-01	2024-12-02	12	t
\.


--
-- Name: subscriptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscriptions_id_seq', 8, true);


--
-- Data for Name: time_table_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.time_table_details (id, time_table_id, day_name, order_number, time_slot, subject_id, staff_id) FROM stdin;
18	13	Monday	1	9:00 - 10:00	1	5
19	13	Monday	2	10 - 11	2	1
20	13	Monday	3	11-12	1	2
\.


--
-- Name: time_table_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.time_table_details_id_seq', 24, true);


--
-- Data for Name: time_tables; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.time_tables (id, school_id, academic_year_id, schools_grades_sections_id) FROM stdin;
13	1	1	1
\.


--
-- Name: time_tables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.time_tables_id_seq', 13, true);


--
-- Data for Name: transports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transports (id, school_id, driver_id, driver_code, vehicle_number, route_number, route_name, vehicle_gps_device_id, vehicle_tracking_url, in_charge_id) FROM stdin;
1	1	1	TESTCODE	KL13T8475	4	TEST EQ	123	12321	4
2	1	4	JAC123	KL86A5035	123	HMT	46456	WETER	5
\.


--
-- Name: transports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transports_id_seq', 34, true);


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (id, user_id, role_id) FROM stdin;
60	7	1
61	1	3
62	1	3
63	1	3
65	2	1
66	10	3
67	11	1
68	4	1
69	4	1
72	5	1
73	7	1
74	7	1
75	1	2
76	1	3
18	2	1
77	1	1
78	10	3
79	10	3
80	10	1
52	10	3
53	4	1
59	1	3
81	24	3
92	25	3
93	25	3
94	25	3
95	25	3
\.


--
-- Name: user_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_roles_id_seq', 95, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, staff_id, student_id, username, password, is_active) FROM stdin;
24	\N	3	sanith2	scrypt:32768:8:1$zflQbflwyU0zpvr1$61e27536fb65491862f04dd7d72fe5341b97edb8517ae8c70f91c3748fe40d1656bb592b1e1cd42703edbce8ed07d65c8115ea0fdfe8451f8df2f093833ae140	t
7	4	\N	jacob	scrypt:32768:8:1$qrrYO6x1vlCu1mJO$ff52cce6b32783a500a3117679b227dafbc482e4cfad9e07c148339b99762f32a50ea999bc77f39574538ebf92cc230410f941f425fea5427fcdf06c8a65239c	t
14	\N	\N	sanith	scrypt:32768:8:1$spt7RPQwLDeJMW51$785beadaac077c27c131cc95d3d1a0039795c390b9a0ec46e43fc65be04f4e86f076e0d11677a2f9756351b8ca2601cca1aefa80f23d7552800c4e6b6546c834	f
15	\N	\N	ishanisanith	scrypt:32768:8:1$KVXMzoIttMxJ3dHk$3ca3dea914065b4e1a3c07777c217c67dc45a00d44e07dfed8558675b7c3ecb615adfaa1632a2515c4e9f326e742349f66b49b054874500c3404d2b6f847d9f6	f
1	\N	\N	sanith1	scrypt:32768:8:1$uW6cdlFECIDadrgf$97414d2d673966913894809ded3698613f3fee35ed13ec4182cc5a102c6aa3bc0351fc89316ece8247cd7f0cad60665e924ec9e1a8ee9c694cfb9f664ce969da	t
10	5	\N	ishani	scrypt:32768:8:1$cYHgBIKSNTpnYoVr$e38fa23e164defdbdf7eeb170304a78b0e59f529bf19aa54c08913a4237abfe3d1276e8c41f149a8a7adb7ffe9ffa19653d1a23acc5a74de2fef0cf014270745	f
16	\N	\N	sanith1	scrypt:32768:8:1$6OaRUMRWpyFOaHSB$546e65e5873ff7033a1d4b2b2ed60f290f603ed66f7dafc1820fe22f39e3b1003e582b2856e167e8db07e4243fa41ce69f4ba31fecf10b3182e84f72f69136ee	f
17	\N	\N	sanith1	scrypt:32768:8:1$WMPETwebGBQs5hr8$8cc85d675f880dac51d0cd6873a725a2f0186747d490c4d1928fbbafa60a3ea1bb789af863906b6063afda09cd3db730abf1f6e3d9fb69c7330932388b3b996a	f
18	\N	\N	sanith1	scrypt:32768:8:1$QtnPPFrxKEfFjnId$0d03469232a2d5244cbb1e592cd3ac111653e46226d5cfadf7844773b5b001437dce2cb49a74d5d6382a2d2776f4b141ab8ab98df8b017d4bcb160eee9c1bda1	f
19	\N	\N	sanith1	scrypt:32768:8:1$mbhceKurL8qbddic$7467821df1456e0297db9feec7e5ad696c5f159372e40e1c9253cded98b13d7c60654d76f38c9f79fb97a03c8fed8548562bd0244ea8ebf37fee4075936eb0bd	f
20	\N	\N	sanith1	scrypt:32768:8:1$PFwvwT31UjtALY5i$2ce738fd99e8a77718004284875ef93d28a4ea5490c30fd8d5f217331839b40e1966bd78ec76954f790bef912f24995b125fa1c6115145584a8c51fd4cce21d8	f
2	\N	\N	Priya	scrypt:32768:8:1$0edyXONXDCkT3yDO$fb3600bf8881165fed7ac1314f74a4a6a7719a6fd95f365ba0f86922790f337702a31681a40bab5a8cbeb61d780794b35af53279330da9dfec2e9c9c41a0bbf7	t
21	\N	\N	sanith1	scrypt:32768:8:1$vhx8CMPjqVtotXuR$a217b0094e4179a41201d696d203e955fe5d768c550bbe97baa2f6b89e38723971101672ae2d7fb0a9574f0f7e19a8c3a2c7154c87e7f6004687745effdb533c	f
22	\N	\N	sanith1	scrypt:32768:8:1$VuS1WNtj0iH2NoiL$9ff201e1d190806f0787622c6d4f6595dee87c93c01c673acf06377ee8ee591b421ee529850aebc49471602dab5c86cb7be3e9f235dfd53987132e4768472c2d	f
4	1	\N	sanithuser	scrypt:32768:8:1$EpuZBvMiL2Hos5PU$01900230a8d1216ee6bd4d0cbd7f24762cad4278f527bb37fe2137d7784c239fd881af3c8a70b56de95ecec7251be83b11cdaabc82d3ff694f32fea397abc32e	t
5	2	\N	priyanp	scrypt:32768:8:1$e867CGlvgvqd1qt8$1898c0852bab3ddb1f24f2b361983994479744cd495e46d8961059b0d5b34ea2a4519006a852cb718c1f68be65926fd3c33653150524af7dbdfff7f610f3e7bd	t
23	\N	6	remya	scrypt:32768:8:1$Q33IWX33lZQNzHTx$f65023f1e718f3f1e82342e26964eb96a25ce834223282e141ad287b19cc1c6ca0640cf45077815a6dcdc10035da68dd1e28e25414eeb936e9ff45f7b787758a	t
13	\N	5	ishanisanith	scrypt:32768:8:1$F0xGlBMJPqB8rKEE$350b6acf21014cd4fa6ffa38128abcfc65dc58e1d5d79356385d0591b59d89c950882a20d3fd8df5914c8fd9c1d891f4b5bcdada73fb7760e1e0de28f06c75ca	t
11	\N	4	asd	scrypt:32768:8:1$gK89pj9kovqsN927$bb0f6b5ab2dba0fa16adb19b26f94fe2df7c9261f6f39bea67f5547a576f3b1e9cb2452e15d1b2e516e7aab6049b8c979d47f91ed3e13a76e829241373532ec6	t
12	\N	\N	asd	scrypt:32768:8:1$oZR9K44DZsHcTmyj$c80a66e6e6dcdd33a84f11d209dac2366706391e8f73e4a819c2e2676b88b0633e13f6f477bbe3dd697ef3dacc93b27bc5b6c021c8bbf30a385565467012d08c	f
25	6	\N	ammu	scrypt:32768:8:1$5vGsYfZyW9CYg2Xn$7e598baf9cabce4f613d0ad93d70203be583de01a5cbf6cf95b4ebad1295fc9307cc846a03ee23e38bbae405d013444af734016726a527fbdafdf728ffb6c212	t
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 25, true);


--
-- Name: academic_years academic_years_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.academic_years
    ADD CONSTRAINT academic_years_pkey PRIMARY KEY (id);


--
-- Name: attendances attendances_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendances
    ADD CONSTRAINT attendances_pkey PRIMARY KEY (id);


--
-- Name: clubs clubs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clubs
    ADD CONSTRAINT clubs_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: exam_mark_details exam_mark_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_mark_details
    ADD CONSTRAINT exam_mark_details_pkey PRIMARY KEY (id);


--
-- Name: exam_marks exam_marks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_marks
    ADD CONSTRAINT exam_marks_pkey PRIMARY KEY (id);


--
-- Name: fee_types fee_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fee_types
    ADD CONSTRAINT fee_types_pkey PRIMARY KEY (id);


--
-- Name: fees fees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fees
    ADD CONSTRAINT fees_pkey PRIMARY KEY (id);


--
-- Name: grades grades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_pkey PRIMARY KEY (id);


--
-- Name: holidays holidays_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_pkey PRIMARY KEY (id);


--
-- Name: houses houses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.houses
    ADD CONSTRAINT houses_pkey PRIMARY KEY (id);


--
-- Name: modules modules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_pkey PRIMARY KEY (id);


--
-- Name: offers offers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.offers
    ADD CONSTRAINT offers_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: school_fee school_fee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_fee
    ADD CONSTRAINT school_fee_pkey PRIMARY KEY (id);


--
-- Name: school_student school_student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_student
    ADD CONSTRAINT school_student_pkey PRIMARY KEY (id);


--
-- Name: school_subscription_module_role_permission school_subscription_module_role_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription_module_role_permission
    ADD CONSTRAINT school_subscription_module_role_permission_pkey PRIMARY KEY (id);


--
-- Name: school_subscription school_subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription
    ADD CONSTRAINT school_subscription_pkey PRIMARY KEY (id);


--
-- Name: schools_grades_sections schools_grades_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools_grades_sections
    ADD CONSTRAINT schools_grades_sections_pkey PRIMARY KEY (id);


--
-- Name: schools schools_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools
    ADD CONSTRAINT schools_pkey PRIMARY KEY (id);


--
-- Name: sections sections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sections
    ADD CONSTRAINT sections_pkey PRIMARY KEY (id);


--
-- Name: staff_types staff_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff_types
    ADD CONSTRAINT staff_types_pkey PRIMARY KEY (id);


--
-- Name: staffs_grades staffs_grades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs_grades
    ADD CONSTRAINT staffs_grades_pkey PRIMARY KEY (id);


--
-- Name: staffs staffs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs
    ADD CONSTRAINT staffs_pkey PRIMARY KEY (id);


--
-- Name: students_grades students_grades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students_grades
    ADD CONSTRAINT students_grades_pkey PRIMARY KEY (id);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- Name: subscription_invoice subscription_invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_invoice
    ADD CONSTRAINT subscription_invoice_pkey PRIMARY KEY (id);


--
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- Name: time_table_details time_table_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_table_details
    ADD CONSTRAINT time_table_details_pkey PRIMARY KEY (id);


--
-- Name: time_tables time_tables_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_tables
    ADD CONSTRAINT time_tables_pkey PRIMARY KEY (id);


--
-- Name: transports transports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transports
    ADD CONSTRAINT transports_pkey PRIMARY KEY (id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: attendances attendances_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendances
    ADD CONSTRAINT attendances_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.staffs(id);


--
-- Name: attendances attendances_schools_grades_sections_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendances
    ADD CONSTRAINT attendances_schools_grades_sections_id_fkey FOREIGN KEY (schools_grades_sections_id) REFERENCES public.schools_grades_sections(id);


--
-- Name: attendances attendances_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendances
    ADD CONSTRAINT attendances_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id);


--
-- Name: attendances attendances_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendances
    ADD CONSTRAINT attendances_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: attendances attendances_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendances
    ADD CONSTRAINT attendances_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.staffs(id);


--
-- Name: clubs clubs_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clubs
    ADD CONSTRAINT clubs_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: events events_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: exam_mark_details exam_mark_details_exam_mark_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_mark_details
    ADD CONSTRAINT exam_mark_details_exam_mark_id_fkey FOREIGN KEY (exam_mark_id) REFERENCES public.exam_marks(id);


--
-- Name: exam_marks exam_marks_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_marks
    ADD CONSTRAINT exam_marks_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.users(id);


--
-- Name: exam_marks exam_marks_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_marks
    ADD CONSTRAINT exam_marks_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: exam_marks exam_marks_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_marks
    ADD CONSTRAINT exam_marks_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id);


--
-- Name: fee_types fee_types_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fee_types
    ADD CONSTRAINT fee_types_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: fees fees_fee_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fees
    ADD CONSTRAINT fees_fee_type_id_fkey FOREIGN KEY (fee_type_id) REFERENCES public.fee_types(id);


--
-- Name: fees fees_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fees
    ADD CONSTRAINT fees_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: grades grades_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: holidays holidays_academic_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_academic_year_id_fkey FOREIGN KEY (academic_year_id) REFERENCES public.academic_years(id);


--
-- Name: holidays holidays_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: houses houses_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.houses
    ADD CONSTRAINT houses_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: modules modules_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.modules(id);


--
-- Name: offers offers_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.offers
    ADD CONSTRAINT offers_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscriptions(id);


--
-- Name: school_fee school_fee_academic_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_fee
    ADD CONSTRAINT school_fee_academic_year_id_fkey FOREIGN KEY (academic_year_id) REFERENCES public.academic_years(id);


--
-- Name: school_fee school_fee_fee_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_fee
    ADD CONSTRAINT school_fee_fee_type_id_fkey FOREIGN KEY (fee_type_id) REFERENCES public.fee_types(id);


--
-- Name: school_student school_student_academic_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_student
    ADD CONSTRAINT school_student_academic_year_id_fkey FOREIGN KEY (academic_year_id) REFERENCES public.academic_years(id);


--
-- Name: school_student school_student_house_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_student
    ADD CONSTRAINT school_student_house_id_fkey FOREIGN KEY (house_id) REFERENCES public.houses(id);


--
-- Name: school_student school_student_school_grade_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_student
    ADD CONSTRAINT school_student_school_grade_section_id_fkey FOREIGN KEY (school_grade_section_id) REFERENCES public.schools_grades_sections(id);


--
-- Name: school_student school_student_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_student
    ADD CONSTRAINT school_student_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: school_student school_student_transport_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_student
    ADD CONSTRAINT school_student_transport_id_fkey FOREIGN KEY (transport_id) REFERENCES public.transports(id);


--
-- Name: school_subscription school_subscription_academic_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription
    ADD CONSTRAINT school_subscription_academic_year_id_fkey FOREIGN KEY (academic_year_id) REFERENCES public.academic_years(id);


--
-- Name: school_subscription_module_role_permission school_subscription_module_role_per_school_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription_module_role_permission
    ADD CONSTRAINT school_subscription_module_role_per_school_subscription_id_fkey FOREIGN KEY (school_subscription_id) REFERENCES public.school_subscription(id);


--
-- Name: school_subscription_module_role_permission school_subscription_module_role_permission_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription_module_role_permission
    ADD CONSTRAINT school_subscription_module_role_permission_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id);


--
-- Name: school_subscription_module_role_permission school_subscription_module_role_permission_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription_module_role_permission
    ADD CONSTRAINT school_subscription_module_role_permission_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- Name: school_subscription_module_role_permission school_subscription_module_role_permission_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription_module_role_permission
    ADD CONSTRAINT school_subscription_module_role_permission_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: school_subscription school_subscription_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription
    ADD CONSTRAINT school_subscription_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: school_subscription school_subscription_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription
    ADD CONSTRAINT school_subscription_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: school_subscription school_subscription_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_subscription
    ADD CONSTRAINT school_subscription_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscriptions(id);


--
-- Name: schools_grades_sections schools_grades_sections_academic_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools_grades_sections
    ADD CONSTRAINT schools_grades_sections_academic_year_id_fkey FOREIGN KEY (academic_year_id) REFERENCES public.academic_years(id);


--
-- Name: schools_grades_sections schools_grades_sections_grade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools_grades_sections
    ADD CONSTRAINT schools_grades_sections_grade_id_fkey FOREIGN KEY (grade_id) REFERENCES public.grades(id);


--
-- Name: schools_grades_sections schools_grades_sections_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools_grades_sections
    ADD CONSTRAINT schools_grades_sections_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: schools_grades_sections schools_grades_sections_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools_grades_sections
    ADD CONSTRAINT schools_grades_sections_section_id_fkey FOREIGN KEY (section_id) REFERENCES public.sections(id);


--
-- Name: sections sections_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sections
    ADD CONSTRAINT sections_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: staffs_grades staffs_grades_class_in_charge_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs_grades
    ADD CONSTRAINT staffs_grades_class_in_charge_id_fkey FOREIGN KEY (class_in_charge_id) REFERENCES public.schools_grades_sections(id);


--
-- Name: staffs_grades staffs_grades_class_in_charge_second_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs_grades
    ADD CONSTRAINT staffs_grades_class_in_charge_second_id_fkey FOREIGN KEY (class_in_charge_second_id) REFERENCES public.schools_grades_sections(id);


--
-- Name: staffs_grades staffs_grades_schools_grades_sections_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs_grades
    ADD CONSTRAINT staffs_grades_schools_grades_sections_id_fkey FOREIGN KEY (schools_grades_sections_id) REFERENCES public.schools_grades_sections(id);


--
-- Name: staffs_grades staffs_grades_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs_grades
    ADD CONSTRAINT staffs_grades_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id);


--
-- Name: staffs_grades staffs_grades_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs_grades
    ADD CONSTRAINT staffs_grades_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id);


--
-- Name: staffs_grades staffs_grades_transport_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs_grades
    ADD CONSTRAINT staffs_grades_transport_id_fkey FOREIGN KEY (transport_id) REFERENCES public.transports(id);


--
-- Name: staffs staffs_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs
    ADD CONSTRAINT staffs_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: staffs staffs_staff_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffs
    ADD CONSTRAINT staffs_staff_type_id_fkey FOREIGN KEY (staff_type_id) REFERENCES public.staff_types(id);


--
-- Name: students_grades students_grades_academic_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students_grades
    ADD CONSTRAINT students_grades_academic_year_id_fkey FOREIGN KEY (academic_year_id) REFERENCES public.academic_years(id);


--
-- Name: students_grades students_grades_schools_grades_sections_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students_grades
    ADD CONSTRAINT students_grades_schools_grades_sections_id_fkey FOREIGN KEY (schools_grades_sections_id) REFERENCES public.schools_grades_sections(id);


--
-- Name: students_grades students_grades_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students_grades
    ADD CONSTRAINT students_grades_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: students_grades students_grades_transport_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students_grades
    ADD CONSTRAINT students_grades_transport_id_fkey FOREIGN KEY (transport_id) REFERENCES public.transports(id);


--
-- Name: students students_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: subjects subjects_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: subscription_invoice subscription_invoice_school_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_invoice
    ADD CONSTRAINT subscription_invoice_school_subscription_id_fkey FOREIGN KEY (school_subscription_id) REFERENCES public.school_subscription(id);


--
-- Name: time_table_details time_table_details_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_table_details
    ADD CONSTRAINT time_table_details_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id);


--
-- Name: time_table_details time_table_details_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_table_details
    ADD CONSTRAINT time_table_details_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id);


--
-- Name: time_table_details time_table_details_time_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_table_details
    ADD CONSTRAINT time_table_details_time_table_id_fkey FOREIGN KEY (time_table_id) REFERENCES public.time_tables(id);


--
-- Name: time_tables time_tables_academic_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_tables
    ADD CONSTRAINT time_tables_academic_year_id_fkey FOREIGN KEY (academic_year_id) REFERENCES public.academic_years(id);


--
-- Name: time_tables time_tables_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_tables
    ADD CONSTRAINT time_tables_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: time_tables time_tables_schools_grades_sections_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.time_tables
    ADD CONSTRAINT time_tables_schools_grades_sections_id_fkey FOREIGN KEY (schools_grades_sections_id) REFERENCES public.schools_grades_sections(id);


--
-- Name: transports transports_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transports
    ADD CONSTRAINT transports_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.staffs(id);


--
-- Name: transports transports_in_charge_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transports
    ADD CONSTRAINT transports_in_charge_id_fkey FOREIGN KEY (in_charge_id) REFERENCES public.staffs(id);


--
-- Name: transports transports_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transports
    ADD CONSTRAINT transports_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id);


--
-- Name: users users_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- PostgreSQL database dump complete
--

