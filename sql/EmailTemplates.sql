--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: utils_emailtemplate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: metrocar
--

SELECT pg_catalog.setval('utils_emailtemplate_id_seq', 9, true);


--
-- Data for Name: utils_emailtemplate; Type: TABLE DATA; Schema: public; Owner: metrocar
--

INSERT INTO utils_emailtemplate VALUES (2, 'REG_REQ_CS', 'REG_REQ_CS', 'Metrocar - Zájem o registraci', 'Vážený/á pane/paní váš zájem o registraci byl zařazen do fronty. O přijetí či zamítnutí registrace budete informováni e-mailem.
Použili jste následující data:
Jméno a příjmení: {{ fields.first_name }} {{ fields.last_name }}
Uživatelské jméno: {{ fields.username }}
Číslo OP: {{ fields.identity_card_number }}
Čislo ŘP: {{ fields.drivers_licence_number }}
Datum narození: {{ fields.date_of_birth }}

V případě nejasností či nesrovnalostí prosíme kontaktuje administrátora serveru Metrocar.
Přejeme pěkný den.');
INSERT INTO utils_emailtemplate VALUES (4, 'REG_DNY_CS', 'REG_DNY_CS', 'Metrocar - Registrace zamítnuta', 'Dobrý den, 
děkujeme za váš zájem o naše služby, bohužel vám, ale musíme oznámit, že vaše registrace na server Metrocar byla zamítnuta.  
Zřejmě jste nesplnil/a některou z podmínek pro použití našich služeb, pro více informací navštivte naše webové stránky.
Děkujeme a nashledanou.');
INSERT INTO utils_emailtemplate VALUES (5, 'RES_SUC_CS', 'RES_SUC_CS', 'Metrocar - Potvrzení přijetí rezervace', 'Dobrý den,
vaše rezervace byla přijata. Vámi vybrané auto bylo rezervováno od {{ fields.reserved_from }} do {{ fields.reserved_until }}.
Děkujeme za použit našich služeb a přejeme pěkný zbytek dne.');
INSERT INTO utils_emailtemplate VALUES (6, 'RES_SUC_EN', 'RES_SUC_EN', 'Metrocar - Reservation succeded', 'Hello,
we would like to inform you, that your reservation request was accepted. The car of choice was reserved from {{ fields.reserved_from }} till {{ fields.reserved_until }}. 
Thanks for using our services. Have a nice day.');
INSERT INTO utils_emailtemplate VALUES (7, 'REG_DNY_EN', 'REG_DNY_EN', 'Metrocar - Registration denied', 'Hello,
thank for applying for our services, but we regretfully inform you that you probably did not meet all our conditions, thus your registration request was denied, for more information visit our website.
Thanks for your time and have a nice day.');
INSERT INTO utils_emailtemplate VALUES (3, 'REG_APP_CS', 'REG_APP_CS', 'Metrocar - Registrace přijata', 'Dobrý den,
dovolujeme si vám oznámit, že vaše registrace na server Metrocar byla přijata. Děkujeme za váš zájem o naše služby.

Pro přihlášní použijte vaše uživateské jméno: {{ fields.username }} a heslo zadané při registraci. Toto heslo si pečlivě uchovejte a nikomu ho neukazujte. V případě ztráty/zapomenutí hesla hesla kontaktujte prosím administrátora.

Pro více informací navštivte naše stránky serveru Metrocar.');
INSERT INTO utils_emailtemplate VALUES (8, 'REG_APP_EN', 'REG_APP_EN', 'Metrocar - Registration approved', 'Hello,
your registration request was approved, you can now login as {{ fields.username }} with password you provided during registration. Please keep your password secret and do not show it to anyone. In case of password loss, please contact administrator.
Thanks for choosing us, have a nice day.');
INSERT INTO utils_emailtemplate VALUES (9, 'REG_REQ_EN', 'REG_REQ_EN', 'Metrocar - Registration request', 'Hello,
we would like to inform you, that your registration request was forwarded to our administration. You will be informed if your registration was denied or approved by email.

You registered with following data:
Name and surname: {{ fields.first_name }} {{ fields.last_name }}
Username: {{ fields.username }}
Identity card number: {{ fields.identity_card_number }}
Driver''s license number: {{ fields.drivers_licence_number }}
Day of birth: {{ fields.date_of_birth }}

In case of discrepancy or any other problem please contact our administration.
Thanks for using our services, have a nice day.');
INSERT INTO utils_emailtemplate VALUES (10, 'REQ_RES_CS', 'REQ_RES_CS', 'Metrocar - Žádost o reset hesla', 'Dobrý den,
Požádal jste o reset vašeho hesla, navštivte prosím následující adresu a vyplňte požadované údaje pro získání nového hesla.
{{ password_reset_url }}');
INSERT INTO utils_emailtemplate VALUES (11, 'REQ_RES_EN', 'REQ_RES_EN', 'Metrocar - Password reset request', 'Hello,
You have requested password reset function, please go to the address below and fill needed values for new password.
{{ password_reset_url }}');

--
-- PostgreSQL database dump complete
--

