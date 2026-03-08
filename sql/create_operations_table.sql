-- Table: public.operations

-- DROP TABLE IF EXISTS public.operations;

CREATE TABLE IF NOT EXISTS public.operations
(
    operation_id bigint NOT NULL DEFAULT nextval('operations_operation_id_seq'::regclass),
    telegram_id bigint NOT NULL,
    amount numeric(10,2) NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT operations_pkey PRIMARY KEY (operation_id),
    CONSTRAINT telegram_id FOREIGN KEY (telegram_id)
        REFERENCES public.users (telegram_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.operations
    OWNER to test;