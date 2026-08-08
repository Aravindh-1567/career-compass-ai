import { useEffect, useState } from "react";

const API = "http://localhost:8000";
const initialSkills = ["HTML","CSS","JavaScript","React","Python","Git"];

export default function App() {
  const [skills,setSkills] = useState(initialSkills);
  const [newSkill,setNewSkill] = useState("");
  const [education,setEducation] = useState("B.Tech CSE");
  const [result,setResult] = useState(null);
  const [jobs,setJobs] = useState([]);
  const [applications,setApplications] = useState([]);
  const [resume,setResume] = useState("");
  const [resumeResult,setResumeResult] = useState(null);
  const [role,setRole] = useState("Full Stack Developer");
  const [questions,setQuestions] = useState([]);
  const [advice,setAdvice] = useState("");
  const [loading,setLoading] = useState(false);

  useEffect(()=>{ fetch(`${API}/api/jobs`).then(r=>r.json()).then(setJobs).catch(()=>{}); loadApplications(); },[]);
  async function loadApplications(){ try{setApplications(await (await fetch(`${API}/api/applications`)).json())}catch{} }

  function addSkill(){
    const x=newSkill.trim();
    if(x && !skills.some(s=>s.toLowerCase()===x.toLowerCase())) setSkills([...skills,x]);
    setNewSkill("");
  }

  async function analyze(){
    setLoading(true);
    try{
      const r=await fetch(`${API}/api/profile/analyze`,{
        method:"POST",headers:{"Content-Type":"application/json"},
        body:JSON.stringify({education,skills,interests:["Technology"]})
      });
      setResult(await r.json());
    } finally { setLoading(false); }
  }

  async function analyzeResume(){
    const r=await fetch(`${API}/api/resume/analyze`,{
      method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({resume})
    });
    setResumeResult(await r.json());
  }

  async function interview(){
    const r=await fetch(`${API}/api/interview`,{
      method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({role,count:5})
    });
    setQuestions((await r.json()).questions);
  }

  async function getAdvice(){
    const r=await fetch(`${API}/api/ai-advice`,{
      method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:"Create a practical 30-day plan to become job-ready."})
    });
    setAdvice((await r.json()).reply);
  }

  async function track(job){
    await fetch(`${API}/api/applications`,{
      method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({title:job.title,company:job.company,status:"Applied",link:""})
    });
    loadApplications();
  }

  return <div className="app">
    <header className="hero">
      <div>
        <span className="eyebrow">AI CAREER PLATFORM</span>
        <h1>CareerCompass <span>AI</span></h1>
        <p>Turn career confusion into a practical path from skills → projects → applications → interviews.</p>
      </div>
      <button className="primary" onClick={getAdvice}>✨ Get AI Career Plan</button>
    </header>

    <main className="grid">
      <section className="card">
        <Title n="01" text="Your Career Profile"/>
        <label>Education</label>
        <input value={education} onChange={e=>setEducation(e.target.value)}/>
        <label>Your skills</label>
        <div className="skills">{skills.map(s=><button className="chip" key={s} onClick={()=>setSkills(skills.filter(x=>x!==s))}>{s} ×</button>)}</div>
        <div className="add"><input value={newSkill} onChange={e=>setNewSkill(e.target.value)} placeholder="Add a skill..."/><button onClick={addSkill}>Add</button></div>
        <button className="primary full" onClick={analyze}>{loading?"Analyzing...":"Analyze My Career Path"}</button>
      </section>

      <section className="card center">
        <Title n="02" text="Job Readiness"/>
        {result ? <>
          <div className="score">{result.readiness_score}<small>%</small></div>
          <p className="muted">Best match: <b>{result.recommended_role}</b></p>
          <div className="progress"><i style={{width:`${result.readiness_score}%`}}/></div>
          <div className="two"><div><b>Matched</b><p>{result.matched_skills.join(", ")||"None"}</p></div><div><b>Gaps</b><p>{result.skill_gaps.join(", ")||"None"}</p></div></div>
        </>:<Empty text="Analyze your profile to see your readiness score."/>}
      </section>

      <section className="card wide">
        <Title n="03" text="Career Paths"/>
        {result ? <div className="careers">{result.career_matches.map(x=><div className="career" key={x.role}><div><b>{x.role}</b><small>{x.matched.length} matched · {x.missing.length} gaps</small></div><strong>{x.score}%</strong></div>)}</div>:<Empty text="Your best career matches will appear here."/>}
      </section>

      <section className="card">
        <Title n="04" text="Skill Gap → Roadmap"/>
        {result?<ul>{result.roadmap.map(x=><li key={x}>{x}</li>)}</ul>:<Empty text="We'll create a practical roadmap from your skill gaps."/>}
      </section>

      <section className="card">
        <Title n="05" text="Practical Projects"/>
        {result?<ul>{result.project_ideas.map(x=><li key={x}>{x}</li>)}</ul>:<Empty text="Project recommendations appear after analysis."/>}
      </section>

      <section className="card wide">
        <Title n="06" text="Internships & Jobs"/>
        <div className="jobs">{jobs.map(j=><div className="job" key={j.id}><div><b>{j.title}</b><small>{j.company} · {j.mode} · {j.type}</small><div className="tags">{j.skills.map(s=><span key={s}>{s}</span>)}</div></div><button className="secondary" onClick={()=>track(j)}>Track Application</button></div>)}</div>
      </section>

      <section className="card">
        <Title n="07" text="Resume Analyzer"/>
        <textarea value={resume} onChange={e=>setResume(e.target.value)} placeholder="Paste resume text here..."/>
        <button className="primary full" onClick={analyzeResume}>Analyze Resume</button>
        {resumeResult&&<div className="result"><b>Resume score: {resumeResult.score}%</b><p>Detected: {resumeResult.detected_skills.join(", ")||"No keywords yet"}</p><p>{resumeResult.suggestions.join(" ")}</p></div>}
      </section>

      <section className="card">
        <Title n="08" text="Interview Coach"/>
        <select value={role} onChange={e=>setRole(e.target.value)}><option>Full Stack Developer</option><option>Frontend Developer</option><option>Python Backend Developer</option><option>AI/ML Engineer</option></select>
        <button className="primary full" onClick={interview}>Generate Questions</button>
        {questions.length>0&&<ol>{questions.map(q=><li key={q}>{q}</li>)}</ol>}
      </section>

      <section className="card wide">
        <Title n="09" text={`Application Tracker (${applications.length})`}/>
        {applications.length?<div className="apps">{applications.map(a=><div key={a.id}><b>{a.title}</b><small>{a.company}</small><em>{a.status}</em></div>)}</div>:<Empty text="Track applications so opportunities don't get lost."/>}
      </section>

      {advice&&<section className="card wide"><Title text="✨ Your AI Career Plan"/><p className="advice">{advice}</p></section>}
    </main>
    <footer>CareerCompass AI · Full-stack portfolio project · Employment outcomes are not guaranteed.</footer>
  </div>
}

function Title({n,text}){return <div className="title">{n&&<small>{n}</small>}<h2>{text}</h2></div>}
function Empty({text}){return <div className="empty">{text}</div>}
