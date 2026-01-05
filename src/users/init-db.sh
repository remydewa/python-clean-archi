#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

  -- Table: public.users

  -- DROP TABLE IF EXISTS public.users;

  CREATE TABLE IF NOT EXISTS public.users
  (
      id uuid NOT NULL DEFAULT gen_random_uuid(),
      email character varying(250) COLLATE pg_catalog."default" NOT NULL,
      password character varying(64) COLLATE pg_catalog."default" NOT NULL,
      is_enabled boolean NOT NULL DEFAULT false,
      creation_date timestamp with time zone NOT NULL DEFAULT now(),
      modification_date timestamp with time zone NOT NULL DEFAULT now(),
      CONSTRAINT users_pkey PRIMARY KEY (id),
      CONSTRAINT users_email_unique UNIQUE (email)
  )

  TABLESPACE pg_default;

  ALTER TABLE IF EXISTS public.users
      OWNER to $POSTGRES_DB;

EOSQL
