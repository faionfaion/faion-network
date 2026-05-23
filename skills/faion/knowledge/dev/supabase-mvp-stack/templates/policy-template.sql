-- purpose: Policy templates scoped to auth.uid() and role.
-- consumes: see content/02-output-contract.xml inputs for supabase-mvp-stack
-- produces: artefact conforming to content/02-output-contract.xml
-- depends-on: content/01-core-rules.xml + content/04-procedure.xml
-- token-budget-impact: ~200-700 tokens when loaded as context

-- Enable RLS
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

-- Select own
CREATE POLICY orders_select_own ON public.orders
FOR SELECT
USING (auth.uid() = user_id);

-- Insert own
CREATE POLICY orders_insert_own ON public.orders
FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Tenant-scoped
CREATE POLICY tenants_select_by_role ON public.tenants
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant', true)::uuid);
