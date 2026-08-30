import { AppShell } from "@/components/AppShell";
import { DashboardClient } from "@/components/DashboardClient";
import { checkApiHealth } from "@/lib/api";

export default async function HomePage() {
  const apiOnline = await checkApiHealth();

  return (
    <AppShell apiOnline={apiOnline}>
      <DashboardClient apiOnline={apiOnline} />
    </AppShell>
  );
}
