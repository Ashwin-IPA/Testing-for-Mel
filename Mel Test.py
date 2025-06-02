// Pharmacist Full Scope of Practice CRM Tool (Excluding Infectious Disease POCT)
 
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Select, SelectItem } from "@/components/ui/select";
 
const CONDITIONS = [
  "Acne", "Asthma", "CVD Risk", "COPD", "Dermatitis", "GORD",
  "Shingles", "Impetigo", "Musculoskeletal Pain", "Nausea/Vomiting",
  "Oral Health", "Otitis Media/Externa", "Obesity", "Psoriasis", "Rhinitis",
  "Smoking Cessation", "Wound Management", "Hormonal Contraception",
  "Travel Health"
];
 
export default function FullScopeCRM() {
  const [form, setForm] = useState({
    patient: {
      fullName: "",
      dob: "",
      gender: "",
      email: "",
      phone: "",
      medicare: "",
      consent: false
    },
    complaint: {
      condition: "",
      description: "",
      duration: "",
      severity: "",
      redFlag: false,
      exclusion: false,
      exclusionReason: ""
    },
    history: {
      medications: "",
      allergies: "",
      chronicConditions: "",
      lifestyle: ""
    },
    assessment: {
      bp: "",
      temp: "",
      hr: "",
      rr: "",
      bmi: "",
      peakFlow: "",
      validatedTool: ""
    },
    plan: {
      diagnosis: "",
      medsPrescribed: "",
      nonPharm: "",
      followUp: "",
      referToGP: false,
      referralReason: "",
      notes: ""
    },
    submitted: false
  });
 
  const updateForm = (section, key, value) => {
    setForm({
      ...form,
      [section]: {
        ...form[section],
        [key]: value
      }
    });
  };
 
  const handleSubmit = () => {
    console.log("CRM Submission:", form);
    setForm({ ...form, submitted: true });
  };
 
  return (
<div className="p-6 max-w-6xl mx-auto space-y-6">
<h1 className="text-3xl font-bold">Pharmacist Full Scope CRM Tool</h1>
 
      <Tabs defaultValue="intake">
<TabsList className="flex flex-wrap gap-2">
<TabsTrigger value="intake">1. Intake</TabsTrigger>
<TabsTrigger value="complaint">2. Complaint</TabsTrigger>
<TabsTrigger value="history">3. History</TabsTrigger>
<TabsTrigger value="assessment">4. Assessment</TabsTrigger>
<TabsTrigger value="plan">5. Plan</TabsTrigger>
</TabsList>
 
        <TabsContent value="intake">
<Card><CardContent className="space-y-3 pt-4">
<Input placeholder="Full Name" value={form.patient.fullName} onChange={e => updateForm("patient", "fullName", e.target.value)} />
<Input type="date" placeholder="DOB" value={form.patient.dob} onChange={e => updateForm("patient", "dob", e.target.value)} />
<Input placeholder="Gender" value={form.patient.gender} onChange={e => updateForm("patient", "gender", e.target.value)} />
<Input placeholder="Email" value={form.patient.email} onChange={e => updateForm("patient", "email", e.target.value)} />
<Input placeholder="Phone" value={form.patient.phone} onChange={e => updateForm("patient", "phone", e.target.value)} />
<Input placeholder="Medicare Number" value={form.patient.medicare} onChange={e => updateForm("patient", "medicare", e.target.value)} />
<div className="flex items-center justify-between">
<label>Consent Provided</label>
<Switch checked={form.patient.consent} onCheckedChange={val => updateForm("patient", "consent", val)} />
</div>
</CardContent></Card>
</TabsContent>
 
        <TabsContent value="complaint">
<Card><CardContent className="space-y-3 pt-4">
<Select value={form.complaint.condition} onValueChange={val => updateForm("complaint", "condition", val)}>
              {CONDITIONS.map(c => <SelectItem key={c} value={c}>{c}</SelectItem>)}
</Select>
<Textarea placeholder="Description" value={form.complaint.description} onChange={e => updateForm("complaint", "description", e.target.value)} />
<Input placeholder="Duration of Symptoms" value={form.complaint.duration} onChange={e => updateForm("complaint", "duration", e.target.value)} />
<Input placeholder="Severity (Mild, Moderate, Severe)" value={form.complaint.severity} onChange={e => updateForm("complaint", "severity", e.target.value)} />
<div className="flex items-center justify-between">
<label>Red Flag Triggered</label>
<Switch checked={form.complaint.redFlag} onCheckedChange={val => updateForm("complaint", "redFlag", val)} />
</div>
<div className="flex items-center justify-between">
<label>Excluded from Protocol</label>
<Switch checked={form.complaint.exclusion} onCheckedChange={val => updateForm("complaint", "exclusion", val)} />
</div>
<Input placeholder="Exclusion Reason" value={form.complaint.exclusionReason} onChange={e => updateForm("complaint", "exclusionReason", e.target.value)} />
</CardContent></Card>
</TabsContent>
 
        <TabsContent value="history">
<Card><CardContent className="space-y-3 pt-4">
<Textarea placeholder="Current Medications" value={form.history.medications} onChange={e => updateForm("history", "medications", e.target.value)} />
<Textarea placeholder="Allergies" value={form.history.allergies} onChange={e => updateForm("history", "allergies", e.target.value)} />
<Textarea placeholder="Chronic Conditions" value={form.history.chronicConditions} onChange={e => updateForm("history", "chronicConditions", e.target.value)} />
<Textarea placeholder="Lifestyle (Smoking, Diet, Exercise)" value={form.history.lifestyle} onChange={e => updateForm("history", "lifestyle", e.target.value)} />
</CardContent></Card>
</TabsContent>
 
        <TabsContent value="assessment">
<Card><CardContent className="space-y-3 pt-4">
<Input placeholder="Blood Pressure (e.g. 120/80)" value={form.assessment.bp} onChange={e => updateForm("assessment", "bp", e.target.value)} />
<Input placeholder="Temperature (°C)" value={form.assessment.temp} onChange={e => updateForm("assessment", "temp", e.target.value)} />
<Input placeholder="Heart Rate (bpm)" value={form.assessment.hr} onChange={e => updateForm("assessment", "hr", e.target.value)} />
<Input placeholder="Respiratory Rate" value={form.assessment.rr} onChange={e => updateForm("assessment", "rr", e.target.value)} />
<Input placeholder="BMI" value={form.assessment.bmi} onChange={e => updateForm("assessment", "bmi", e.target.value)} />
<Input placeholder="Peak Flow (L/min)" value={form.assessment.peakFlow} onChange={e => updateForm("assessment", "peakFlow", e.target.value)} />
<Input placeholder="Validated Tool Result (e.g. ACT Score)" value={form.assessment.validatedTool} onChange={e => updateForm("assessment", "validatedTool", e.target.value)} />
</CardContent></Card>
</TabsContent>
 
        <TabsContent value="plan">
<Card><CardContent className="space-y-3 pt-4">
<Input placeholder="Diagnosis" value={form.plan.diagnosis} onChange={e => updateForm("plan", "diagnosis", e.target.value)} />
<Textarea placeholder="Medications Prescribed" value={form.plan.medsPrescribed} onChange={e => updateForm("plan", "medsPrescribed", e.target.value)} />
<Textarea placeholder="Non-Pharmacological Advice" value={form.plan.nonPharm} onChange={e => updateForm("plan", "nonPharm", e.target.value)} />
<Input placeholder="Follow-Up Timeframe (e.g. 1 week)" value={form.plan.followUp} onChange={e => updateForm("plan", "followUp", e.target.value)} />
<div className="flex items-center justify-between">
<label>GP Referral Required</label>
<Switch checked={form.plan.referToGP} onCheckedChange={val => updateForm("plan", "referToGP", val)} />
</div>
<Textarea placeholder="Referral Reason or Plan Notes" value={form.plan.referralReason} onChange={e => updateForm("plan", "referralReason", e.target.value)} />
<Textarea placeholder="Final Notes / Summary" value={form.plan.notes} onChange={e => updateForm("plan", "notes", e.target.value)} />
<Button className="w-full" onClick={handleSubmit}>Submit & Generate Summary</Button>
</CardContent></Card>
</TabsContent>
</Tabs>
</div>
  );
}
