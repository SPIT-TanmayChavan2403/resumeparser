import { useState, useRef } from "react";
import s from './Scorer.module.css'
import { json } from "react-router-dom";

export default function Scorer(props) {
    const [files, setFiles] = useState([])
    const [result, setResult] = useState([])
    const [jd, setJD] = useState("")
    const inputRef = useRef(null);
    const [preloader, setPreloader] = useState(false)
    const [resStatus, setResStatus] = useState(false)
    const [selectedValue, setSelectedValue] = useState("BERT")

    const handleAlgoChange = (e) => {
        console.log("Changing value to...", e.target.value)
        setSelectedValue(e.target.value)
    }

    const takeFiles = (e) => {
        const data = new FormData();
        setFiles(inputRef.current.files);
    }

    const upload = (e) => {
        setResult([])
        setResStatus(false)
        setPreloader(true)
        const data = new FormData();
        for (let i = 0; i < files.length; i++) {
            data.append(`image ${i}`, files[i]);
        }
        data.append("job_description", jd)
        data.append("algo", selectedValue)

        fetch("http://localhost:5000/upload", {
            method: "POST",
            body: data,
            // body: JSON.stringify({files: data, jobDescription: jd}),
        }).then(res => res.json())
        .then(data => {
            setResult(data);
            setPreloader(false)
            setResStatus(true)
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
                    <select name="cars" id="cars" onChange={handleAlgoChange} value={selectedValue}>
                        <option value="BERT">BERT</option>
                        <option value="TF-IDF">TF-IDF</option>
                    </select>
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
                {
                    !resStatus && !preloader && <h2>Upload files to calculate</h2>
                }
                {
                    resStatus && <ul>
                                    {Array.from(result).map(file => {
                                        return <li key={file}>{file}</li>
                                    })}
                                </ul>
                }
                {
                    preloader && <img src="preloader.gif"></img>
                }
            </div>
        </div>
    );
}