/**
 * Tabbed prototype UI for SmartGORE Atacama / NemoClaw (same programme family as
 * ../presentacion_smartgore_atacama_nemoclaw.html).
 * Bundler/build not wired in this static repo; kept as a design/source reference only.
 */
import { useState } from "react";

const sections = ["Desafío", "NemoClaw", "Plan 6 Meses", "Presupuesto"];

const accent = "#00C4B4";
const dark = "#0B1F3A";
const mid = "#112D52";
const light = "#E8F4FD";

const styles = {
  wrap: {
    fontFamily: "'Georgia', 'Times New Roman', serif",
    background: `linear-gradient(160deg, ${dark} 0%, ${mid} 100%)`,
    minHeight: "100vh",
    color: "#E8F4FD",
    padding: "0 0 3rem",
  },
  hero: {
    background: `linear-gradient(135deg, #061626 0%, #0B2D52 60%, #0D3D6B 100%)`,
    padding: "2.5rem 2rem 2rem",
    borderBottom: `2px solid ${accent}`,
    position: "relative",
    overflow: "hidden",
  },
  heroTagline: {
    fontFamily: "'Arial Narrow', Arial, sans-serif",
    fontSize: "11px",
    letterSpacing: "4px",
    textTransform: "uppercase",
    color: accent,
    marginBottom: "0.5rem",
  },
  heroTitle: {
    fontFamily: "'Arial Black', Arial, sans-serif",
    fontSize: "clamp(1.6rem, 4vw, 2.6rem)",
    fontWeight: 900,
    color: "#FFFFFF",
    margin: "0 0 0.25rem",
    lineHeight: 1.1,
  },
  heroSub: {
    fontFamily: "'Arial Narrow', Arial, sans-serif",
    fontSize: "clamp(0.85rem, 2vw, 1.05rem)",
    color: "#8EC8F0",
    marginBottom: "1.5rem",
    letterSpacing: "1px",
  },
  statsRow: {
    display: "flex",
    gap: "1rem",
    flexWrap: "wrap",
    marginTop: "1rem",
  },
  stat: {
    background: "rgba(0,196,180,0.12)",
    border: `1px solid rgba(0,196,180,0.4)`,
    borderRadius: "8px",
    padding: "0.6rem 1rem",
    textAlign: "center",
  },
  statNum: {
    fontFamily: "'Arial Black', Arial, sans-serif",
    fontSize: "1.5rem",
    fontWeight: 900,
    color: accent,
    display: "block",
  },
  statLabel: {
    fontFamily: "'Arial Narrow', Arial, sans-serif",
    fontSize: "10px",
    letterSpacing: "1.5px",
    textTransform: "uppercase",
    color: "#8EC8F0",
  },
  nav: {
    display: "flex",
    background: "#071828",
    borderBottom: "1px solid rgba(0,196,180,0.2)",
    overflowX: "auto",
  },
  navBtn: (active) => ({
    fontFamily: "'Arial Narrow', Arial, sans-serif",
    fontSize: "12px",
    letterSpacing: "2px",
    textTransform: "uppercase",
    padding: "0.9rem 1.4rem",
    border: "none",
    borderBottom: active ? `3px solid ${accent}` : "3px solid transparent",
    background: "transparent",
    color: active ? accent : "#8EC8F0",
    cursor: "pointer",
    fontWeight: active ? 700 : 400,
    whiteSpace: "nowrap",
    transition: "color 0.2s",
  }),
  body: {
    padding: "2rem 1.5rem",
    maxWidth: "760px",
    margin: "0 auto",
  },
  sectionTitle: {
    fontFamily: "'Arial Black', Arial, sans-serif",
    fontSize: "1.4rem",
    fontWeight: 900,
    color: "#FFFFFF",
    marginBottom: "0.25rem",
    marginTop: 0,
  },
  sectionSub: {
    fontFamily: "'Arial Narrow', Arial, sans-serif",
    fontSize: "0.9rem",
    color: accent,
    letterSpacing: "2px",
    textTransform: "uppercase",
    marginBottom: "1.5rem",
  },
  card: {
    background: "rgba(255,255,255,0.05)",
    border: "1px solid rgba(0,196,180,0.25)",
    borderRadius: "12px",
    padding: "1.25rem 1.5rem",
    marginBottom: "1rem",
  },
  cardTitle: {
    fontFamily: "'Arial Black', Arial, sans-serif",
    fontSize: "0.95rem",
    fontWeight: 900,
    color: "#FFFFFF",
    marginBottom: "0.4rem",
    marginTop: 0,
  },
  cardBody: {
    fontFamily: "'Georgia', serif",
    fontSize: "0.88rem",
    color: "#B0CDE8",
    lineHeight: 1.7,
    margin: 0,
  },
  badge: (color) => ({
    display: "inline-block",
    fontFamily: "'Arial Narrow', Arial, sans-serif",
    fontSize: "10px",
    letterSpacing: "1.5px",
    textTransform: "uppercase",
    padding: "3px 10px",
    borderRadius: "20px",
    background: color === "teal" ? "rgba(0,196,180,0.15)" : color === "amber" ? "rgba(255,180,50,0.15)" : "rgba(100,180,255,0.15)",
    border: `1px solid ${color === "teal" ? "rgba(0,196,180,0.5)" : color === "amber" ? "rgba(255,180,50,0.5)" : "rgba(100,180,255,0.5)"}`,
    color: color === "teal" ? accent : color === "amber" ? "#FFB432" : "#64B4FF",
    marginBottom: "0.5rem",
    marginRight: "0.5rem",
  }),
  divider: {
    border: "none",
    borderTop: "1px solid rgba(0,196,180,0.2)",
    margin: "1.5rem 0",
  },
  timelineItem: (color) => ({
    display: "flex",
    gap: "1rem",
    marginBottom: "1.25rem",
    position: "relative",
  }),
  dot: (color) => ({
    width: "36px",
    height: "36px",
    borderRadius: "50%",
    background: color,
    border: `2px solid rgba(255,255,255,0.2)`,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "'Arial Black', Arial, sans-serif",
    fontSize: "12px",
    fontWeight: 900,
    color: "#fff",
    flexShrink: 0,
  }),
  budgetRow: (highlight) => ({
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "0.6rem 0",
    borderBottom: "1px solid rgba(0,196,180,0.1)",
    background: highlight ? "rgba(0,196,180,0.06)" : "transparent",
    borderRadius: highlight ? "4px" : "0",
    paddingLeft: highlight ? "8px" : "0",
    paddingRight: highlight ? "8px" : "0",
  }),
  budgetLabel: {
    fontFamily: "'Arial Narrow', Arial, sans-serif",
    fontSize: "0.85rem",
    color: "#B0CDE8",
  },
  budgetAmt: (highlight) => ({
    fontFamily: "'Arial Black', Arial, sans-serif",
    fontSize: highlight ? "1rem" : "0.9rem",
    fontWeight: 900,
    color: highlight ? accent : "#E8F4FD",
  }),
};

const months = [
  {
    num: "1–2",
    color: "#1A6B8A",
    label: "Diagnóstico y Fundaciones",
    goals: "Levantamiento de procesos críticos, definición de arquitectura NemoClaw, capacitación inicial equipo TI y directivos.",
    deliverables: [
      "Mapa de procesos con índice de aceleración IAGen por unidad",
      "Instalación y configuración de NemoClaw en infraestructura del GORE",
      "Taller directivo: IA para decisiones de gestión regional (16 hrs)",
      "Taller técnico TI: arquitectura, seguridad y gobernanza de datos (24 hrs)",
    ],
    module: "Módulos 3 y 4 — Transparencia y Control Financiero (piloto)",
  },
  {
    num: "3–4",
    color: "#0E7C6B",
    label: "Pilotos y Primeras Ganancias",
    goals: "Despliegue de 3 módulos prioritarios con equipos reales. Ajuste iterativo. Capacitación operativa.",
    deliverables: [
      "Módulo 1 activo: IA para Fondos Concursables — revisión y scoring automático",
      "Módulo 2 activo: Chatbot institucional ciudadano 24/7 (OIRs y consultas)",
      "Módulo 4 activo: Control financiero y detección de inconsistencias",
      "Programa 'NemoClaw Academy' — 80 funcionarios certificados nivel básico",
      "Dashboard de KPIs operacionales en tiempo real",
    ],
    module: "Módulos 1, 2 y 4 operativos",
  },
  {
    num: "5–6",
    color: "#176B3F",
    label: "Escala y Consolidación",
    goals: "Extensión a todos los módulos, cocreación de aplicaciones sectoriales, evaluación de impacto.",
    deliverables: [
      "Módulos 5–8 desplegados: proyectos FNDR, monitoreo territorial, auditoría",
      "Hackathon interno: 4 aplicaciones co-diseñadas con funcionarios y ciudadanos",
      "40 funcionarios certificados nivel avanzado (prompt engineering y análisis de datos)",
      "Informe de impacto: horas ahorradas, reducción de errores, NPS ciudadano",
      "Roadmap 2026–2027 basado en resultados",
    ],
    module: "Módulos 5, 6, 7 y 8 operativos — 8/8 módulos activos",
  },
];

const budgetItems = [
  { cat: "Licencias NemoClaw (6 meses, hasta 300 usuarios)", amt: "$48.000.000", usd: "~USD 52k" },
  { cat: "Infraestructura cloud y seguridad de datos", amt: "$18.000.000", usd: "~USD 20k" },
  { cat: "Integración con sistemas GORE (SAP, SIF, Mercado Público)", amt: "$22.000.000", usd: "~USD 24k" },
  { cat: "Capacitación y certificación (NemoClaw Academy, 120 funcionarios)", amt: "$15.000.000", usd: "~USD 16k" },
  { cat: "Hackathon y co-desarrollo de aplicaciones (mes 5–6)", amt: "$8.000.000", usd: "~USD 9k" },
  { cat: "Consultoría especializada en IA pública (CENIA / Stanford liaison)", amt: "$14.000.000", usd: "~USD 15k" },
  { cat: "Comunicaciones, gestión del cambio y difusión ciudadana", amt: "$5.000.000", usd: "~USD 5k" },
  { cat: "Contingencia (10%)", amt: "$13.000.000", usd: "~USD 14k" },
];

function Desafio() {
  return (
    <div>
      <p style={styles.sectionSub}>El contexto</p>
      <h2 style={styles.sectionTitle}>Un Gobierno Regional que debe hacer más con los mismos recursos</h2>
      <p style={{ ...styles.cardBody, marginBottom: "1.5rem", fontSize: "0.93rem" }}>
        El Gobierno Regional de Atacama administra una de las regiones más extensas y con mayor actividad minera del país, enfrentando
        una demanda creciente de servicios, rendición de fondos FNDR, atención ciudadana y cumplimiento normativo — con una dotación
        de funcionarios que no crece al mismo ritmo.
      </p>

      <div style={styles.card}>
        <span style={styles.badge("teal")}>Evidencia CENIA–SOFOFA 2024</span>
        <p style={styles.cardTitle}>El 84% de las tareas del sector público es aceleerable con IA</p>
        <p style={styles.cardBody}>
          El estudio sobre IAGen en Chile (CENIA, SOFOFA, Stanford 2024) revela que los especialistas en gestión de políticas
          públicas tienen el índice de aceleración más alto de todos los empleos analizados: <strong style={{ color: accent }}>0,84</strong>.
          Esto significa que 4 de cada 5 tareas que realiza un funcionario GORE podrían ejecutarse en la mitad del tiempo
          sin pérdida de calidad, usando herramientas de IA generativa ya disponibles hoy.
        </p>
      </div>

      <div style={styles.card}>
        <span style={styles.badge("blue")}>Valor económico</span>
        <p style={styles.cardTitle}>USD 1.100 millones anuales de oportunidad en el sector público chileno</p>
        <p style={styles.cardBody}>
          El mismo estudio estima que los empleos del sector público de gestión y asesoría concentran un Valor IA de USD 1,1 billón
          anuales a nivel nacional. Para el GORE Atacama, con cerca de 2.400 funcionarios, esto equivale a una oportunidad
          de eficiencia de <strong style={{ color: accent }}>USD 12–18 millones anuales</strong> en tiempo recuperado para funciones de mayor valor.
        </p>
      </div>

      <hr style={styles.divider} />

      <p style={styles.sectionSub}>Problemas concretos</p>
      {[
        { t: "Fondos Concursables saturados", b: "La revisión manual de postulaciones FNDR y fondos regionales consume semanas de trabajo técnico. Errores documentales retrasan desembolsos críticos para comunas." },
        { t: "Atención ciudadana desbordada", b: "Las OIRs reciben miles de consultas repetitivas. Sin automatización, los tiempos de respuesta superan los plazos legales en períodos de alta demanda." },
        { t: "Control financiero reactivo", b: "La detección de inconsistencias en convenios y transferencias ocurre post-facto. La IA puede anticipar anomalías antes de que escalen." },
        { t: "Carga administrativa docente y social", b: "Profesionales del trabajo social y educadores que trabajan para el GORE dedican hasta 36 horas semanales a tareas administrativas acelerables." },
      ].map((d, i) => (
        <div key={i} style={{ display: "flex", gap: "0.75rem", marginBottom: "0.85rem", alignItems: "flex-start" }}>
          <div style={{ width: "8px", height: "8px", borderRadius: "50%", background: accent, marginTop: "8px", flexShrink: 0 }} />
          <div>
            <p style={{ ...styles.cardTitle, fontSize: "0.9rem", marginBottom: "0.2rem" }}>{d.t}</p>
            <p style={{ ...styles.cardBody, fontSize: "0.84rem" }}>{d.b}</p>
          </div>
        </div>
      ))}

      <div style={{ ...styles.card, background: "rgba(0,196,180,0.08)", borderColor: "rgba(0,196,180,0.5)", marginTop: "1.5rem" }}>
        <p style={{ ...styles.cardTitle, color: accent }}>La oportunidad histórica</p>
        <p style={styles.cardBody}>
          Chile está en la transición de la digitalización a la <em>inteligización</em>. El GORE Atacama puede convertirse en el
          primer gobierno regional del país en desplegar IA generativa en los 8 procesos críticos de gestión,
          posicionándose como modelo para las 15 regiones restantes y la transformación digital del Estado.
        </p>
      </div>
    </div>
  );
}

function Nemoclaw() {
  const feats = [
    { icon: "🏛️", t: "Diseñado para el sector público chileno", b: "NemoClaw cumple con la Ley 21.180 de Transformación Digital del Estado y el Marco de Ciberseguridad del CISO Nacional. Sus datos se procesan en servidores soberanos en Chile." },
    { icon: "🔗", t: "Integración nativa con ecosistema GORE", b: "Conectores preconfigurados con Mercado Público, SIF, plataformas de rendición SUBDERE y ChileAtiende. No requiere desarrollo a medida para los flujos más comunes." },
    { icon: "🧠", t: "Modelos entrenados en normativa chilena", b: "Los LLMs de NemoClaw incorporan el Estatuto Administrativo, Ley de Compras Públicas, Ley del Lobby, normativa GORE y guías de Contraloría como contexto base." },
    { icon: "📊", t: "Módulos SmartGore 4.0 out-of-the-box", b: "Los 8 módulos de la arquitectura SmartGore (fondos, OIRs, transparencia, control financiero, proyectos, monitoreo territorial, FNDR y auditoría) vienen preconfigurados y listos para parametrizar." },
    { icon: "🎓", t: "NemoClaw Academy integrada", b: "Plataforma de capacitación on-line con rutas diferenciadas por perfil: directivo, técnico, profesional y operativo. Certificación reconocida por el SENCE." },
    { icon: "🔍", t: "Explicabilidad y auditoría de decisiones IA", b: "Cada recomendación del sistema incluye trazabilidad: qué datos usó, con qué certeza y qué normativa aplicó. Esencial para control de Contraloría." },
    { icon: "📡", t: "Monitoreo territorial con IA geoespacial", b: "Integración con imágenes satelitales Sentinel-2 y sensores IoT para el módulo de monitoreo agrícola, minero y ambiental de la Región de Atacama." },
    { icon: "🤝", t: "Modelo de co-implementación colaborativo", b: "NemoClaw incluye un equipo de implementación residente durante los primeros 6 meses, trabajando con los equipos GORE para asegurar adopción real, no solo instalación técnica." },
  ];
  return (
    <div>
      <p style={styles.sectionSub}>La plataforma</p>
      <h2 style={styles.sectionTitle}>Por qué NemoClaw para el GORE Atacama</h2>
      <p style={{ ...styles.cardBody, marginBottom: "1.5rem", fontSize: "0.93rem" }}>
        NemoClaw es la plataforma de IA generativa diseñada específicamente para gobiernos regionales y servicios públicos chilenos.
        A diferencia de soluciones genéricas, NemoClaw parte del contexto normativo y operacional del Estado chileno,
        reduciendo drásticamente el tiempo de implementación y los riesgos de compliance.
      </p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "0.85rem" }}>
        {feats.map((f, i) => (
          <div key={i} style={styles.card}>
            <p style={{ fontSize: "1.5rem", margin: "0 0 0.4rem" }}>{f.icon}</p>
            <p style={styles.cardTitle}>{f.t}</p>
            <p style={styles.cardBody}>{f.b}</p>
          </div>
        ))}
      </div>
      <hr style={styles.divider} />
      <div style={{ ...styles.card, background: "rgba(0,196,180,0.08)", borderColor: "rgba(0,196,180,0.5)" }}>
        <p style={styles.sectionSub}>Comparativa clave</p>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.82rem", fontFamily: "'Arial Narrow', Arial, sans-serif" }}>
            <thead>
              <tr>
                {["Criterio", "NemoClaw", "Solución genérica", "Desarrollo a medida"].map((h, i) => (
                  <th key={i} style={{ textAlign: "left", padding: "0.5rem 0.75rem", borderBottom: "1px solid rgba(0,196,180,0.4)", color: i === 1 ? accent : "#8EC8F0", fontWeight: i === 1 ? 700 : 400 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                ["Normativa chilena incorporada", "✅ Nativa", "❌ Manual", "⚠️ Costoso"],
                ["Tiempo de despliegue", "4–6 semanas", "3–6 meses", "12–18 meses"],
                ["Módulos SmartGore", "8 preconfigurados", "0", "Desde cero"],
                ["Capacitación incluida", "✅ Academy", "❌ Extra costo", "❌ Extra costo"],
                ["Costo total 6 meses", "USD ~155k", "USD ~200k+", "USD ~400k+"],
              ].map((row, i) => (
                <tr key={i} style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                  {row.map((cell, j) => (
                    <td key={j} style={{ padding: "0.45rem 0.75rem", color: j === 1 ? "#E8F4FD" : "#8EC8F0" }}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function Plan() {
  return (
    <div>
      <p style={styles.sectionSub}>Hoja de ruta</p>
      <h2 style={styles.sectionTitle}>Plan progresivo de 6 meses</h2>
      <p style={{ ...styles.cardBody, marginBottom: "1.5rem", fontSize: "0.93rem" }}>
        La implementación sigue la lógica de «ganancias rápidas primero» recomendada por el estudio CENIA–SOFOFA:
        comenzar con los módulos de mayor Valor IA y menor complejidad operativa, generar confianza interna
        y evidencia, y escalar progresivamente.
      </p>

      {months.map((m, idx) => (
        <div key={idx} style={{ marginBottom: "2rem" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.85rem" }}>
            <div style={styles.dot(m.color)}>M{m.num}</div>
            <div>
              <p style={{ margin: 0, fontFamily: "'Arial Black', Arial, sans-serif", fontSize: "1rem", color: "#FFFFFF" }}>{m.label}</p>
              <p style={{ margin: 0, fontFamily: "'Arial Narrow', Arial, sans-serif", fontSize: "11px", letterSpacing: "2px", textTransform: "uppercase", color: accent }}>Meses {m.num}</p>
            </div>
          </div>
          <div style={styles.card}>
            <span style={styles.badge("teal")}>{m.module}</span>
            <p style={{ ...styles.cardBody, marginBottom: "0.75rem" }}>{m.goals}</p>
            <ul style={{ margin: 0, paddingLeft: "1.2rem" }}>
              {m.deliverables.map((d, i) => (
                <li key={i} style={{ ...styles.cardBody, marginBottom: "0.35rem" }}>{d}</li>
              ))}
            </ul>
          </div>
        </div>
      ))}

      <hr style={styles.divider} />
      <p style={styles.sectionSub}>Capacitación detallada</p>
      <h3 style={{ ...styles.sectionTitle, fontSize: "1.1rem" }}>NemoClaw Academy — 120 funcionarios en 3 perfiles</h3>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "0.85rem", marginTop: "1rem" }}>
        {[
          { perfil: "Directivo", horas: "16 hrs", contenido: "IA estratégica, interpretación de dashboards, gestión del cambio, toma de decisiones basadas en datos.", participantes: "24 directivos" },
          { perfil: "Profesional técnico", horas: "40 hrs", contenido: "Uso avanzado de NemoClaw, prompt engineering, validación de outputs IA, cocreación de flujos automatizados.", participantes: "48 profesionales" },
          { perfil: "Operativo / Administrativo", horas: "24 hrs", contenido: "Manejo de módulos específicos, interpretación de alertas, registro y gestión documental asistida por IA.", participantes: "48 funcionarios" },
        ].map((p, i) => (
          <div key={i} style={styles.card}>
            <span style={styles.badge("amber")}>{p.horas}</span>
            <p style={styles.cardTitle}>{p.perfil}</p>
            <p style={{ ...styles.cardBody, fontSize: "0.82rem", marginBottom: "0.5rem" }}>{p.contenido}</p>
            <p style={{ fontFamily: "'Arial Narrow', Arial, sans-serif", fontSize: "11px", color: accent, letterSpacing: "1px" }}>{p.participantes}</p>
          </div>
        ))}
      </div>

      <hr style={styles.divider} />
      <p style={styles.sectionSub}>Co-desarrollo de aplicaciones</p>
      <h3 style={{ ...styles.sectionTitle, fontSize: "1.1rem" }}>Hackathon SmartGore Atacama (Mes 5)</h3>
      <div style={styles.card}>
        <p style={styles.cardBody}>
          Durante 48 horas, equipos mixtos de funcionarios, profesionales TI del GORE y estudiantes de la UCN Antofagasta y
          Universidad de Atacama co-diseñan aplicaciones NemoClaw para problemas específicos de la región. Los 4 mejores
          prototipos reciben financiamiento para desarrollo completo en el segundo semestre.
        </p>
        <div style={{ marginTop: "0.75rem", display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {["Alertas tempranas de proyectos FNDR en riesgo", "Asistente de postulaciones para comunidades indígenas", "Monitor ambiental minero con IA satelital", "Chatbot de orientación laboral para mujeres rurales"].map((t, i) => (
            <span key={i} style={styles.badge("blue")}>{t}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

function Presupuesto() {
  const total = 143_000_000;
  const conting = 13_000_000;
  const gran = total + conting;
  return (
    <div>
      <p style={styles.sectionSub}>Inversión total</p>
      <h2 style={styles.sectionTitle}>Presupuesto estimado — 6 meses</h2>
      <div style={{ ...styles.stat, textAlign: "left", marginBottom: "1.5rem", padding: "1rem 1.5rem" }}>
        <span style={{ ...styles.statLabel, display: "block", marginBottom: "0.25rem" }}>Inversión total programa (incl. contingencia)</span>
        <span style={{ ...styles.statNum, fontSize: "2rem" }}>$156.000.000 CLP</span>
        <span style={{ fontFamily: "'Arial Narrow', Arial, sans-serif", fontSize: "12px", color: "#8EC8F0" }}>≈ USD 169.000 | ≈ 0,4% del presupuesto regional anual</span>
      </div>

      <div style={styles.card}>
        {budgetItems.map((item, i) => (
          <div key={i} style={styles.budgetRow(false)}>
            <span style={styles.budgetLabel}>{item.cat}</span>
            <div style={{ textAlign: "right" }}>
              <span style={styles.budgetAmt(false)}>{item.amt}</span>
              <span style={{ fontFamily: "'Arial Narrow', Arial, sans-serif", fontSize: "10px", color: "#5A8AAA", display: "block" }}>{item.usd}</span>
            </div>
          </div>
        ))}
        <div style={{ ...styles.budgetRow(true), marginTop: "0.5rem", borderBottom: "none" }}>
          <span style={{ ...styles.budgetLabel, color: accent, fontWeight: 700 }}>TOTAL PROGRAMA</span>
          <div style={{ textAlign: "right" }}>
            <span style={styles.budgetAmt(true)}>$156.000.000</span>
            <span style={{ fontFamily: "'Arial Narrow', Arial, sans-serif", fontSize: "10px", color: accent, display: "block" }}>≈ USD 169k</span>
          </div>
        </div>
      </div>

      <hr style={styles.divider} />
      <p style={styles.sectionSub}>Retorno esperado</p>
      <h3 style={{ ...styles.sectionTitle, fontSize: "1.1rem" }}>ROI del programa — año 1</h3>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "0.75rem", marginBottom: "1.5rem" }}>
        {[
          { v: "36hrs/sem", l: "Tiempo docente recuperado por prof.", color: accent },
          { v: "~2.400", l: "Funcionarios beneficiados", color: "#64B4FF" },
          { v: "USD 12M", l: "Valor IA potencial anual GORE Atacama", color: "#FFB432" },
          { v: "ROI 7x", l: "Estimado primer año (horas → valor)", color: "#90E890" },
        ].map((s, i) => (
          <div key={i} style={styles.stat}>
            <span style={{ ...styles.statNum, color: s.color }}>{s.v}</span>
            <span style={styles.statLabel}>{s.l}</span>
          </div>
        ))}
      </div>

      <div style={styles.card}>
        <span style={styles.badge("teal")}>Fuente de financiamiento sugerida</span>
        <p style={styles.cardTitle}>Cobertura presupuestaria</p>
        <p style={styles.cardBody}>
          El programa puede financiarse mediante tres fuentes complementarias: <strong style={{ color: "#E8F4FD" }}>Fondo Regional de Innovación y Competitividad (FRIC)</strong> del GORE — ítem transformación digital;
          <strong style={{ color: "#E8F4FD" }}> Fondos FNDR Subtítulo 33</strong> para capacitación y desarrollo de capital humano; y postulación al
          <strong style={{ color: "#E8F4FD" }}> Programa de Transformación Digital del Estado</strong> (SEGPRES–Ministerio de Ciencia), que cofinancia
          proyectos piloto de IA en instituciones públicas hasta en un 40% de su costo total.
        </p>
      </div>

      <div style={{ ...styles.card, background: "rgba(0,196,180,0.08)", borderColor: "rgba(0,196,180,0.5)", marginTop: "0.75rem" }}>
        <p style={styles.cardTitle}>Nota metodológica</p>
        <p style={{ ...styles.cardBody, fontSize: "0.82rem" }}>
          Los valores se basan en el índice de aceleración 0,84 para especialistas en políticas públicas (CENIA–SOFOFA 2024),
          aplicado a la dotación estimada del GORE Atacama, con salario promedio de funcionarios del sector público según CASEN 2022
          y encuesta DIPRES 2024. El Valor IA anual se calcula como: dotación × salario promedio × índice de aceleración × 12 meses.
          Los costos NemoClaw son referenciales para efectos de planificación presupuestaria.
        </p>
      </div>
    </div>
  );
}

export default function App() {
  const [active, setActive] = useState(0);

  const views = [<Desafio />, <Nemoclaw />, <Plan />, <Presupuesto />];

  return (
    <div style={styles.wrap}>
      <div style={styles.hero}>
        <div style={{ position: "absolute", top: 0, right: 0, width: "300px", height: "100%", background: "radial-gradient(ellipse at 80% 50%, rgba(0,196,180,0.08) 0%, transparent 70%)", pointerEvents: "none" }} />
        <p style={styles.heroTagline}>Gobierno Regional de Atacama · Programa Estratégico IA 2025</p>
        <h1 style={styles.heroTitle}>SmartGORE Atacama<br /><span style={{ color: accent }}>con NemoClaw</span></h1>
        <p style={styles.heroSub}>De la digitalización a la inteligización — Un plan de 6 meses</p>
        <div style={styles.statsRow}>
          {[
            { n: "0,84", l: "Índice aceleración IA sector público" },
            { n: "8", l: "Módulos SmartGORE desplegados" },
            { n: "120", l: "Funcionarios capacitados" },
            { n: "6 meses", l: "De diagnóstico a plena operación" },
          ].map((s, i) => (
            <div key={i} style={styles.stat}>
              <span style={styles.statNum}>{s.n}</span>
              <span style={styles.statLabel}>{s.l}</span>
            </div>
          ))}
        </div>
      </div>

      <nav style={styles.nav}>
        {sections.map((s, i) => (
          <button key={i} style={styles.navBtn(active === i)} onClick={() => setActive(i)}>{s}</button>
        ))}
      </nav>

      <div style={styles.body}>{views[active]}</div>

      <div style={{ textAlign: "center", padding: "1rem", fontFamily: "'Arial Narrow', Arial, sans-serif", fontSize: "11px", letterSpacing: "2px", color: "rgba(142,200,240,0.4)" }}>
        GORE ATACAMA · SMARTGORE 4.0 · NEMOCLAW · MAYO 2025
      </div>
    </div>
  );
}
