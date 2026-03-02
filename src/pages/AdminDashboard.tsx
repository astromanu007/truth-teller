import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { supabase } from "@/integrations/supabase/runtime-client";
import { Header } from "@/components/Header";
import {
  Shield, Users, BarChart3, Activity, TrendingUp,
  AlertTriangle, CheckCircle, Loader2, ArrowLeft
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table, TableBody, TableCell, TableHead,
  TableHeader, TableRow
} from "@/components/ui/table";

interface Profile {
  user_id: string;
  full_name: string | null;
  email: string | null;
  created_at: string;
}

interface Analysis {
  id: string;
  news_text: string;
  prediction: string;
  confidence: number;
  created_at: string;
  user_id: string;
}

const AdminDashboard = () => {
  const { user, isAdmin, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [users, setUsers] = useState<Profile[]>([]);
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalAnalyses: 0,
    fakeCount: 0,
    realCount: 0,
  });

  useEffect(() => {
    if (!authLoading && (!user || !isAdmin)) {
      navigate("/");
    }
  }, [user, isAdmin, authLoading, navigate]);

  useEffect(() => {
    if (isAdmin) fetchData();
  }, [isAdmin]);

  const fetchData = async () => {
    setLoading(true);

    const [profilesRes, analysesRes] = await Promise.all([
      supabase.from("profiles").select("*"),
      supabase.from("analysis_history").select("*").order("created_at", { ascending: false }).limit(50),
    ]);

    const profileData = profilesRes.data || [];
    const analysisData = analysesRes.data || [];

    setUsers(profileData);
    setAnalyses(analysisData);
    setStats({
      totalUsers: profileData.length,
      totalAnalyses: analysisData.length,
      fakeCount: analysisData.filter((a) => a.prediction === "FAKE").length,
      realCount: analysisData.filter((a) => a.prediction === "REAL").length,
    });
    setLoading(false);
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gradient-hero flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  const statCards = [
    { label: "Total Users", value: stats.totalUsers, icon: Users, color: "text-primary" },
    { label: "Total Analyses", value: stats.totalAnalyses, icon: BarChart3, color: "text-primary" },
    { label: "Detected Real", value: stats.realCount, icon: CheckCircle, color: "text-[hsl(142,70%,45%)]" },
    { label: "Detected Fake", value: stats.fakeCount, icon: AlertTriangle, color: "text-[hsl(0,84%,60%)]" },
  ];

  return (
    <div className="min-h-screen bg-gradient-hero">
      <Header />

      <main className="container mx-auto px-4 py-8">
        {/* Title */}
        <div className="flex items-center gap-4 mb-8">
          <Button variant="ghost" size="icon" onClick={() => navigate("/")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
              <Shield className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Admin Dashboard</h1>
              <p className="text-sm text-muted-foreground">Monitor users and analysis activity</p>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {statCards.map((stat, i) => (
            <div key={i} className="bg-card rounded-xl p-6 border border-border/50 card-elevated">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm text-muted-foreground">{stat.label}</span>
                <stat.icon className={`w-5 h-5 ${stat.color}`} />
              </div>
              <p className="text-3xl font-bold text-foreground">{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Users Table */}
        <div className="bg-card rounded-xl border border-border/50 card-elevated mb-8">
          <div className="p-6 border-b border-border/50">
            <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
              <Users className="w-5 h-5 text-primary" />
              Registered Users
            </h2>
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Joined</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={3} className="text-center text-muted-foreground py-8">
                    No users yet
                  </TableCell>
                </TableRow>
              ) : (
                users.map((u) => (
                  <TableRow key={u.user_id}>
                    <TableCell className="font-medium">{u.full_name || "—"}</TableCell>
                    <TableCell>{u.email || "—"}</TableCell>
                    <TableCell>{new Date(u.created_at).toLocaleDateString()}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>

        {/* Analysis History */}
        <div className="bg-card rounded-xl border border-border/50 card-elevated">
          <div className="p-6 border-b border-border/50">
            <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" />
              Recent Analyses
            </h2>
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Text</TableHead>
                <TableHead>Result</TableHead>
                <TableHead>Confidence</TableHead>
                <TableHead>Date</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {analyses.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="text-center text-muted-foreground py-8">
                    No analyses yet
                  </TableCell>
                </TableRow>
              ) : (
                analyses.map((a) => (
                  <TableRow key={a.id}>
                    <TableCell className="max-w-[300px] truncate">{a.news_text}</TableCell>
                    <TableCell>
                      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                        a.prediction === "REAL"
                          ? "bg-[hsl(142,70%,45%)]/20 text-[hsl(142,70%,45%)]"
                          : "bg-[hsl(0,84%,60%)]/20 text-[hsl(0,84%,60%)]"
                      }`}>
                        {a.prediction === "REAL" ? <CheckCircle className="w-3 h-3" /> : <AlertTriangle className="w-3 h-3" />}
                        {a.prediction}
                      </span>
                    </TableCell>
                    <TableCell>{a.confidence}%</TableCell>
                    <TableCell>{new Date(a.created_at).toLocaleDateString()}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;
