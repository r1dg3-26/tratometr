-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    telegram_id bigint NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    balance numeric(10,2) NOT NULL DEFAULT 0,
    timezone numeric(2,0) NOT NULL DEFAULT 3,
    CONSTRAINT users_pkey PRIMARY KEY (telegram_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to test;