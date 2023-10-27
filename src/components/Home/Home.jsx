import React from "react";
import s from "./Home.module.css";

export default function Home(){
    return(
        <div id={s.wrapper}>
            <div id={s.leftSection}>
                <h1>TAKE CONTROL</h1>
                <h3>of your</h3>
                <h1>JOB SEARCH</h1>
                <h3>with simple and quick Resume Score</h3>
                <a href="/score">
                    <button>
                        Start Scoring...
                    </button>
                </a>
                <img src="blob.svg" alt="Geometry" />
            </div>
            <div id={s.rightSection}>
                <div id={s.imageContainer} />
                <img src="bannerImg.png" alt="Parser image" />  
            </div>
        </div>
    )
}   