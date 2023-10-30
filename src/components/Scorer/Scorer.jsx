import { useState, useRef } from "react";
import s from './Scorer.module.css'
import { json } from "react-router-dom";

export default function Scorer(props) {
    const [files, setFiles] = useState([])
    const [result, setResult] = useState([])
    const [jd, setJD] = useState("")
    const inputRef = useRef(null);

    const takeFiles = (e) => {
        const data = new FormData();
        setFiles(inputRef.current.files);
    }

    const upload = (e) => {
        const data = new FormData();
        for (let i = 0; i < files.length; i++) {
            data.append(`image ${i}`, files[i]);
        }

        fetch("https://20.243.20.210:5000/upload", {
            method: "POST",
            body: data,
            // body: JSON.stringify({files: data, jobDescription: jd}),
        }).then(res => res.json()).then(data => {
            let tempres = [];
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    tempres.push(`Score of ${key} is: ${data[key]}`);
                }
            }
            setResult(tempres);
        }).catch(err => {
            console.log(err);
        })
    }

    const handleJD = (e) => {
        setJD(e.target.value)
    }

    return (
        <div id={s.wrapper}>
            <div id={s.top_section}>
                <div id={s.jd_container}>
                    <h2>Enter Job Description</h2>
                    <textarea value={jd} name="" id="" cols="30" rows="5" onChange={handleJD} ></textarea>
                </div>
                <div id={s.resume_container}>
                    <h2>Upload Resume</h2>
                    
                    <button onClick={() => {inputRef.current.click()}}>Select Files</button>
                    <input onChange={takeFiles} ref={inputRef} type="file" multiple  id={s.inputField} />
                    <button onClick={upload}>Upload</button>
                    <div id={s.resume_list}>
                        <ul>
                            {Array.from(files).map(file => {
                                return <li key={file.name}>{file.name}</li>
                            })}
                        </ul>
                    </div>
                </div>
            </div>
            <div id={s.bottom_section}>
                <ul>
                        {Array.from(result).map(file => {
                            return <li key={file}>{file}</li>
                        })}
                </ul>
            </div>
        </div>
    );
}