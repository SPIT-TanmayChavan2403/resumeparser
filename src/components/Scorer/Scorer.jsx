import { useState } from "react";


export default function Scorer(props) {
    const [files, setFiles] = useState([])

    const takeInput = (e) => {
        const data = new FormData();
        setFiles(e.target.files);
        console.log(e.target.files)
    }

    const upload = (e) => {
        const data = new FormData();
        for (let i = 0; i < files.length; i++) {
            data.append(`image ${i}`, files[i]);
        }
        fetch("http://localhost:5000/upload", {
            method: "POST",
            body: data
        }).then(res => res.json()).then(data => {
            console.log(data);
        }).catch(err => {
            console.log(err);
        })
    }

    return (
        <div className="scorer">
            <input type="file" multiple onChange={takeInput} />
            <button onClick={upload}>Upload</button>
        </div>
    );
}