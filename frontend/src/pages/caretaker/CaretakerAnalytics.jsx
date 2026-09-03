import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
    FaArrowLeft,
    FaChartBar,
    FaUsers,
    FaExclamationTriangle,
    FaHeartbeat,
    FaCalendarAlt,
    FaChartLine,
    FaStethoscope,
    FaHospital
} from "react-icons/fa";
import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    PieChart,
    Pie,
    Cell,
    LineChart,
    Line,
    CartesianGrid,
    Legend
} from "recharts";

import { getCaretakerAnalytics } from "../../services/caretakerService";
import { useToast } from "../../context/ToastContext";

import "../../styles/Patient.css";
import "../../styles/Dashboard.css";
import "../../styles/Button.css";

const RISK_COLORS = {
    High: "#ef4444",
    Medium: "#f59e0b",
    Low: "#10b981"
};

const PIE_COLORS = ["#38bdf8", "#818cf8", "#c084fc", "#f472b6", "#fb923c", "#4ade80", "#2dd4bf"];

function CaretakerAnalytics() {
    const { showToast } = useToast();
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadAnalyticsData();
    }, []);

    const loadAnalyticsData = async () => {
        try {
            setLoading(true);
            const data = await getCaretakerAnalytics();
            setAnalytics(data);
        } catch (error) {
            console.error("Failed to load caretaker analytics:", error);
            showToast("Failed to load analytics data.", "error");
        } finally {
            setLoading(false);
        }
    };

    const riskPieData = analytics?.risk_distribution
        ? Object.entries(analytics.risk_distribution).map(([key, val]) => ({
              name: `${key} Risk`,
              value: val
          }))
        : [];

    return (
        <div className="patient-dashboard">
            <div className="dashboard-overlay"></div>

            <div className="dashboard-content">
                <Link
                    to="/caretaker/dashboard"
                    className="secondary-btn"
                    style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "10px",
                        marginBottom: "25px"
                    }}
                >
                    <FaArrowLeft />
                    Back to Dashboard
                </Link>

                <section className="dashboard-hero">
                    <div className="hero-content">
                        <div className="dashboard-brand">
                            <FaHospital />
                            MedAssist AI
                        </div>
                        <h1>Caretaker Analytics & Health Trends</h1>
                        <p>
                            Comprehensive clinical analytics, disease distributions, risk
                            stratification, and consultation trends across all your assigned patients.
                        </p>
                    </div>

                    <div className="hero-image">
                        <div className="hero-icon-circle">
                            <FaChartBar />
                        </div>
                    </div>
                </section>

                {loading ? (
                    <div className="glass-card" style={{ marginTop: "30px", textAlign: "center", padding: "50px" }}>
                        <h2>Loading Analytics & Patient Trends...</h2>
                    </div>
                ) : (
                    <>
                        {/* KPI STATS */}
                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                                gap: "20px",
                                marginTop: "35px"
                            }}
                        >
                            <div className="stat-card">
                                <FaUsers size={28} color="#38bdf8" />
                                <h3>{analytics?.total_patients || 0}</h3>
                                <span>Total Assigned Patients</span>
                            </div>

                            <div className="stat-card">
                                <FaExclamationTriangle size={28} color="#ef4444" />
                                <h3>{analytics?.high_risk_count || 0}</h3>
                                <span>High-Risk Patient Cases</span>
                            </div>

                            <div className="stat-card">
                                <FaHeartbeat size={28} color="#c084fc" />
                                <h3>{analytics?.total_predictions || 0}</h3>
                                <span>Total AI Disease Predictions</span>
                            </div>

                            <div className="stat-card">
                                <FaStethoscope size={28} color="#4ade80" />
                                <h3>{analytics?.recent_activity?.length || 0}</h3>
                                <span>Recent Consultations</span>
                            </div>
                        </div>

                        {/* CHARTS ROW 1: Disease Distribution & Risk Breakdown */}
                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns: "repeat(auto-fit, minmax(380px, 1fr))",
                                gap: "25px",
                                marginTop: "40px"
                            }}
                        >
                            {/* Disease Distribution Bar Chart */}
                            <div className="glass-card">
                                <div className="section-header" style={{ marginBottom: "20px" }}>
                                    <h2>Top Diagnosed Conditions</h2>
                                    <p>Frequency of AI predicted diseases among your assigned patients</p>
                                </div>

                                {analytics?.disease_distribution?.length > 0 ? (
                                    <div style={{ width: "100%", height: 300 }}>
                                        <ResponsiveContainer>
                                            <BarChart data={analytics.disease_distribution}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                                                <XAxis
                                                    dataKey="disease"
                                                    stroke="#94a3b8"
                                                    tick={{ fill: "#cbd5e1", fontSize: 11 }}
                                                    interval={0}
                                                    angle={-20}
                                                    textAnchor="end"
                                                    height={60}
                                                />
                                                <YAxis stroke="#94a3b8" tick={{ fill: "#cbd5e1", fontSize: 12 }} allowDecimals={false} />
                                                <Tooltip
                                                    contentStyle={{
                                                        backgroundColor: "rgba(15, 23, 42, 0.95)",
                                                        borderColor: "#38bdf8",
                                                        borderRadius: "8px",
                                                        color: "#fff"
                                                    }}
                                                />
                                                <Bar dataKey="count" fill="#38bdf8" radius={[6, 6, 0, 0]} name="Patient Cases" />
                                            </BarChart>
                                        </ResponsiveContainer>
                                    </div>
                                ) : (
                                    <p style={{ color: "#94a3b8", textAlign: "center", padding: "40px 0" }}>
                                        No disease predictions logged for assigned patients yet.
                                    </p>
                                )}
                            </div>

                            {/* Risk Stratification Pie Chart */}
                            <div className="glass-card">
                                <div className="section-header" style={{ marginBottom: "20px" }}>
                                    <h2>Patient Risk Stratification</h2>
                                    <p>Proportion of high, medium, and low risk patient assessments</p>
                                </div>

                                {riskPieData.some((d) => d.value > 0) ? (
                                    <div style={{ width: "100%", height: 300 }}>
                                        <ResponsiveContainer>
                                            <PieChart>
                                                <Pie
                                                    data={riskPieData}
                                                    dataKey="value"
                                                    nameKey="name"
                                                    cx="50%"
                                                    cy="50%"
                                                    outerRadius={100}
                                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                                >
                                                    {riskPieData.map((entry, index) => {
                                                        const color =
                                                            entry.name.includes("High")
                                                                ? RISK_COLORS.High
                                                                : entry.name.includes("Medium")
                                                                ? RISK_COLORS.Medium
                                                                : RISK_COLORS.Low;
                                                        return <Cell key={`cell-${index}`} fill={color} />;
                                                    })}
                                                </Pie>
                                                <Tooltip
                                                    contentStyle={{
                                                        backgroundColor: "rgba(15, 23, 42, 0.95)",
                                                        borderColor: "#38bdf8",
                                                        borderRadius: "8px",
                                                        color: "#fff"
                                                    }}
                                                />
                                                <Legend />
                                            </PieChart>
                                        </ResponsiveContainer>
                                    </div>
                                ) : (
                                    <p style={{ color: "#94a3b8", textAlign: "center", padding: "40px 0" }}>
                                        No risk assessments recorded for assigned patients yet.
                                    </p>
                                )}
                            </div>
                        </div>

                        {/* CHARTS ROW 2: Activity Timeline & Recent Feed */}
                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns: "repeat(auto-fit, minmax(380px, 1fr))",
                                gap: "25px",
                                marginTop: "30px"
                            }}
                        >
                            {/* Monthly Trends */}
                            <div className="glass-card">
                                <div className="section-header" style={{ marginBottom: "20px" }}>
                                    <h2>Consultation & Disease Trends</h2>
                                    <p>Monthly timeline of patient predictions and medical checkups</p>
                                </div>

                                <div style={{ width: "100%", height: 260 }}>
                                    <ResponsiveContainer>
                                        <LineChart data={analytics?.monthly_trends || []}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                                            <XAxis dataKey="month" stroke="#94a3b8" tick={{ fill: "#cbd5e1" }} />
                                            <YAxis stroke="#94a3b8" tick={{ fill: "#cbd5e1" }} allowDecimals={false} />
                                            <Tooltip
                                                contentStyle={{
                                                    backgroundColor: "rgba(15, 23, 42, 0.95)",
                                                    borderColor: "#38bdf8",
                                                    borderRadius: "8px",
                                                    color: "#fff"
                                                }}
                                            />
                                            <Line
                                                type="monotone"
                                                dataKey="consultations"
                                                stroke="#38bdf8"
                                                strokeWidth={3}
                                                dot={{ r: 5, fill: "#38bdf8" }}
                                                activeDot={{ r: 8 }}
                                                name="Activity Count"
                                            />
                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            {/* Recent Patient Activity Feed */}
                            <div className="glass-card">
                                <div className="section-header" style={{ marginBottom: "20px" }}>
                                    <h2>Recent Patient Activity</h2>
                                    <p>Latest health events and AI prediction alerts</p>
                                </div>

                                {analytics?.recent_activity?.length > 0 ? (
                                    <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                                        {analytics.recent_activity.map((act, i) => (
                                            <div
                                                key={i}
                                                style={{
                                                    display: "flex",
                                                    justifyContent: "space-between",
                                                    alignItems: "center",
                                                    padding: "12px 16px",
                                                    borderRadius: "10px",
                                                    background: "rgba(255, 255, 255, 0.05)",
                                                    border: "1px solid rgba(255, 255, 255, 0.08)"
                                                }}
                                            >
                                                <div>
                                                    <h4 style={{ color: "#ffffff", margin: 0 }}>{act.patient_name}</h4>
                                                    <span style={{ color: "#38bdf8", fontSize: "13px" }}>
                                                        Predicted: {act.predicted_disease}
                                                    </span>
                                                </div>
                                                <small style={{ color: "#94a3b8" }}>
                                                    {new Date(act.created_at).toLocaleDateString()}
                                                </small>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <p style={{ color: "#94a3b8", textAlign: "center", padding: "40px 0" }}>
                                        No recent patient activity.
                                    </p>
                                )}
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}

export default CaretakerAnalytics;
