import React from 'react'
import { clientData } from '../../data/data'
import Image from 'next/image'

export default function ClientOne() {
  return (
        <div className="row justify-content-center gx-4 gy-4">
            {clientData.map((item,index)=>( 
                <div className="col-xl-4 col-lg-4 col-md-6" key={index}>
                    <div className="jobstock-reviews-box">
                        <div className="jobstock-reviews-desc">
                            <h6 className="review-title-yui">{item.title}</h6>
                            <p>{item.desc}</p>
                        </div>
                        <div className="jobstock-reviews-flex">
                            <div className="jobstock-reviews-thumb">
                                <div className="jobstock-reviews-figure"><Image src={item.image} width={0} height={0} sizes='100vw' style={{width:'100%', height:'auto'}} className="img-fluid circle" alt=""/></div>
                            </div>
                            <div className="jobstock-reviews-caption">
                                <div className="jobstock-reviews-title"><h4>{item.name}</h4></div>
                                <div className="jobstock-reviews-designation"><span>{item.position}</span></div>
                                <div className="jobstock-reviews-rates">
                                    <i className="fa-solid fa-star"></i>
                                    <i className="fa-solid fa-star"></i>
                                    <i className="fa-solid fa-star"></i>
                                    <i className="fa-solid fa-star"></i>
                                    <i className="fa-solid fa-star deactive"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
  )
}
