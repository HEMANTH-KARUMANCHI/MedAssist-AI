import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

import {
    FaArrowLeft,
    FaFileMedical,
    FaCloudUploadAlt,
    FaFolderOpen,
    FaHeartbeat,
    FaFilePdf,
    FaNotesMedical,
    FaDownload,
    FaTrashAlt,
    FaSpinner
} from "react-icons/fa";

import {
    getPatientReports,
    uploadPatientReport,
    downloadPatientReport,
    deletePatientReport
} from "../../services/patientService";
import { useToast } from "../../context/ToastContext";

import "../../styles/Dashboard.css";
import "../../styles/Button.css";
import "../../styles/Form.css";
import "../../styles/Patient.css";

function HealthReports() {
    const { showToast } = useToast();
    const [selectedFile, setSelectedFile] = useState(null);
    const [reportType, setReportType] = useState("");
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);

    const fetchReports = async () => {
        try {
            setLoading(true);
            const data = await getPatientReports();
            setReports(data.reports || []);
        } catch (err) {
            console.error("Fetch reports error:", err);
            showToast("Failed to fetch reports list", "error");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchReports();
    }, []);

    const handleFileChange = (event) => {
        if (event.target.files && event.target.files[0]) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            showToast("Please select a report file to upload.", "warning");
            return;
        }

        try {
            setUploading(true);
            await uploadPatientReport(selectedFile);
            showToast("Report uploaded successfully!", "success");
            setSelectedFile(null);
            setReportType("");
            const fileInput = document.getElementById("reportUpload");
            if (fileInput) fileInput.value = "";
            await fetchReports();
        } catch (err) {
            console.error("Upload error:", err);
            showToast(err.response?.data?.detail || "Failed to upload report.", "error");
        } finally {
            setUploading(false);
        }
    };

    const handleDownload = async (report) => {
        try {
            await downloadPatientReport(report.id, report.file_name);
            showToast("Report download started", "info");
        } catch (err) {
            console.error("Download error:", err);
            showToast(err.response?.data?.detail || "Failed to download report.", "error");
        }
    };

    const handleDelete = async (reportId) => {
        if (!window.confirm("Are you sure you want to delete this report?")) {
            return;
        }

        try {
            await deletePatientReport(reportId);
            setReports((prev) => prev.filter((r) => r.id !== reportId));
            showToast("Report deleted successfully.", "success");
        } catch (err) {
            console.error("Delete error:", err);
            showToast(err.response?.data?.detail || "Failed to delete report.", "error");
        }
    };

    const formatFileSize = (bytes) => {
        if (!bytes && bytes !== 0) return "N/A";
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
        return (bytes / (1024 * 1024)).toFixed(2) + " MB";
    };

    const formatDate = (dateStr) => {
        if (!dateStr) return "N/A";
        try {
            return new Date(dateStr).toLocaleDateString(undefined, {
                year: "numeric",
                month: "short",
                day: "numeric"
            });
        } catch {
            return dateStr;
        }
    };

    const formatFileType = (mimeType, fileName) => {
        if (mimeType?.includes("pdf") || fileName?.endsWith(".pdf")) {
            return "PDF Document";
        }
        if (mimeType?.includes("image") || fileName?.match(/\.(jpg|jpeg|png)$/i)) {
            return "Medical Image";
        }
        return mimeType || "Document";
    };

    return (
        <div className="patient-dashboard">
            <div className="dashboard-overlay"></div>

            <div className="dashboard-content">
                <Link
                    to="/patient/dashboard"
                    className="back-button"
                >
                    <FaArrowLeft />
                    Back to Dashboard
                </Link>

                <section className="dashboard-hero">
                    <div className="hero-left">
                        <div className="dashboard-brand">
                            <FaFileMedical />
                            MedAssist AI
                        </div>

                        <h1>Health Reports</h1>

                        <p>
                            Securely upload, organize and access all your
                            medical reports in one place. Maintain a complete
                            digital health history for faster diagnosis and
                            better treatment.
                        </p>
                    </div>

                    <div className="hero-right">
                        <div className="hero-badge">
                            <FaCloudUploadAlt />
                            Reports
                        </div>
                    </div>
                </section>

                <section className="stats-grid">
                    <div className="stats-card">
                        <FaFolderOpen />
                        <h3>Total Reports</h3>
                        <h2>{reports.length}</h2>
                    </div>

                    <div className="stats-card">
                        <FaCloudUploadAlt />
                        <h3>Upload Status</h3>
                        <h2>{uploading ? "Uploading..." : "Ready"}</h2>
                    </div>

                    <div className="stats-card">
                        <FaHeartbeat />
                        <h3>Health Records</h3>
                        <h2>Secure</h2>
                    </div>

                    <div className="stats-card">
                        <FaNotesMedical />
                        <h3>Medical Files</h3>
                        <h2>Digital</h2>
                    </div>
                </section>

                <div className="dashboard-grid">
                    <div className="glass-card">
                        <div className="section-header">
                            <div>
                                <h2>Upload New Report</h2>
                                <p>
                                    Upload laboratory reports, prescriptions,
                                    scans and other medical documents securely.
                                </p>
                            </div>
                        </div>

                        <div className="form-grid">
                            <div className="form-group">
                                <label>Report Category</label>
                                <select
                                    className="form-input"
                                    value={reportType}
                                    onChange={(e) => setReportType(e.target.value)}
                                >
                                    <option value="">Select Category (Optional)</option>
                                    <option>Blood Test</option>
                                    <option>X-Ray</option>
                                    <option>MRI Scan</option>
                                    <option>CT Scan</option>
                                    <option>ECG</option>
                                    <option>Prescription</option>
                                    <option>Discharge Summary</option>
                                    <option>Other</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Medical Report File (PDF, JPG, PNG - Max 10MB)</label>
                                <input
                                    id="reportUpload"
                                    className="form-input"
                                    type="file"
                                    accept=".pdf,.jpg,.jpeg,.png"
                                    onChange={handleFileChange}
                                />
                            </div>
                        </div>

                        {selectedFile && (
                            <div className="selected-file-card">
                                <FaFilePdf />
                                <div>
                                    <strong>{selectedFile.name}</strong>
                                    <p>{formatFileSize(selectedFile.size)} - Ready for upload</p>
                                </div>
                            </div>
                        )}

                        <div className="action-buttons">
                            <button
                                className="primary-btn"
                                onClick={handleUpload}
                                disabled={uploading || !selectedFile}
                                style={{
                                    display: "inline-flex",
                                    alignItems: "center",
                                    gap: "8px",
                                    opacity: uploading || !selectedFile ? 0.7 : 1
                                }}
                            >
                                {uploading ? (
                                    <>
                                        <FaSpinner className="fa-spin" /> Uploading...
                                    </>
                                ) : (
                                    <>
                                        <FaCloudUploadAlt /> Upload Report
                                    </>
                                )}
                            </button>
                        </div>
                    </div>

                    <div className="glass-card">
                        <div className="section-header">
                            <div>
                                <h2>Upload Guidelines</h2>
                                <p>Tips for maintaining your digital medical records.</p>
                            </div>
                        </div>

                        <div className="prediction-features">
                            <div className="feature-item">
                                ✅ Upload clear PDF or image files (JPG, PNG).
                            </div>
                            <div className="feature-item">
                                ✅ File size must not exceed 10 MB per file.
                            </div>
                            <div className="feature-item">
                                ✅ Keep reports updated after every doctor visit.
                            </div>
                            <div className="feature-item">
                                ✅ Your reports remain encrypted and securely stored.
                            </div>
                            <div className="feature-item">
                                ✅ Download or review your uploaded files at any time.
                            </div>
                        </div>
                    </div>
                </div>

                <div className="glass-card" style={{ marginTop: "24px" }}>
                    <div className="section-header">
                        <div>
                            <h2>Uploaded Reports</h2>
                            <p>View, download, and manage all your medical records.</p>
                        </div>
                    </div>

                    {loading ? (
                        <div style={{ textAlign: "center", padding: "40px", color: "#94a3b8" }}>
                            <p>Loading your medical reports...</p>
                        </div>
                    ) : reports.length === 0 ? (
                        <div className="empty-state">
                            <FaFileMedical size={60} />
                            <h3>No Reports Uploaded</h3>
                            <p>
                                Upload your first medical report above to maintain
                                your digital health records.
                            </p>
                        </div>
                    ) : (
                        <div className="table-responsive">
                            <table className="dashboard-table">
                                <thead>
                                    <tr>
                                        <th>File Name</th>
                                        <th>Type</th>
                                        <th>Size</th>
                                        <th>Uploaded On</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {reports.map((report) => (
                                        <tr key={report.id}>
                                            <td>
                                                <div className="file-cell">
                                                    <FaFilePdf />
                                                    <span>{report.file_name}</span>
                                                </div>
                                            </td>

                                            <td>
                                                <span className="status-badge info">
                                                    {formatFileType(report.file_type, report.file_name)}
                                                </span>
                                            </td>

                                            <td>{formatFileSize(report.file_size)}</td>

                                            <td>{formatDate(report.uploaded_at)}</td>

                                            <td>
                                                <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
                                                    <button
                                                        onClick={() => handleDownload(report)}
                                                        title="Download Report"
                                                        style={{
                                                            background: "rgba(59, 130, 246, 0.2)",
                                                            border: "1px solid rgba(59, 130, 246, 0.4)",
                                                            color: "#60a5fa",
                                                            padding: "6px 12px",
                                                            borderRadius: "6px",
                                                            cursor: "pointer",
                                                            display: "inline-flex",
                                                            alignItems: "center",
                                                            gap: "6px",
                                                            fontSize: "13px"
                                                        }}
                                                    >
                                                        <FaDownload /> Download
                                                    </button>

                                                    <button
                                                        onClick={() => handleDelete(report.id)}
                                                        title="Delete Report"
                                                        style={{
                                                            background: "rgba(239, 68, 68, 0.2)",
                                                            border: "1px solid rgba(239, 68, 68, 0.4)",
                                                            color: "#f87171",
                                                            padding: "6px 12px",
                                                            borderRadius: "6px",
                                                            cursor: "pointer",
                                                            display: "inline-flex",
                                                            alignItems: "center",
                                                            gap: "6px",
                                                            fontSize: "13px"
                                                        }}
                                                    >
                                                        <FaTrashAlt /> Delete
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default HealthReports;