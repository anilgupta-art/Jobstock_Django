import React from 'react'
import Link from 'next/link'
import Image from 'next/image'

import { aboutData } from '../data/data'
import NavBgWhite from '../components/navbar/nav-bg-white'
import FormTwo from '../components/form/form-two'
import FeatureJob from '../components/job/feature-job'
import HireBox from '../components/cta/hire-box'
import CtaOne from '../components/cta/cta-one'
import PricingOne from '../components/pricing/pricing-one'
import FooterLight from '../components/footer/footer-light'
import ScrollToTop from '../components/scroll-to-top'
import RangeSlider from '../components/range-slider'

export default function HomeSix() {
  return (
    <>
        <NavBgWhite/>   

        <div className="image-cover hero-header p-150" style={{backgroundImage:`url('/img/slider-2.jpg')`, backgroundColor:'#016551', backgroundRepeat:'no-repeat'}}>
            <div className="container">
                <div className="row">
                    <div className="col-xl-7 col-lg-9 col-md-12">
                        <div className="simple-search-wrap mb-5">
                            <div className="hero-search-2">
                                <h2 className="text-xl text-main">Find</h2>
                                <h1 className="mb-4">Great Job Opportunity<br/>You Deserve</h1>
                                <div className="search-from-clasic mt-5">
                                    <FormTwo/>
                                </div>
                            </div>
                        </div>
                        
                        <div className="vesm-rsv-box-wrap">
                            <div className="vesm-rsv-box-head">
                                <div className="vesm-rsv-txt"><span>14k reviews on</span></div>
                                <div className="vesm-rsv-star">
                                    <i className="fa-solid fa-star"></i>
                                    <i className="fa-solid fa-star"></i>
                                    <i className="fa-solid fa-star"></i>
                                    <i className="fa-solid fa-star"></i>
                                    <i className="fa-solid fa-star"></i>
                                </div>
                            </div>
                            <div className="vesm-rsv-box-caption">
                                <div className="vesm-rsv-elcox">
                                    <div className="vesm-rsv-elcox-01"><span className="vshm-arrows"><i className="fa-solid fa-share"></i></span><h5 className="reviews-ctr">4.9</h5></div>
                                </div>
                                <div className="vesm-rsv-elcox-02">
                                    <ul>
                                        <li><figure><Image src='/img/user-3.png' width={36} height={36} className="img-fluid" alt=""/></figure></li>
                                        <li><figure><Image src='/img/user-7.png' width={36} height={36} className="img-fluid" alt=""/></figure></li>
                                        <li><figure><Image src='/img/user-5.png' width={36} height={36} className="img-fluid" alt=""/></figure></li>
                                        <li><figure><Image src='/img/user-6.png' width={36} height={36} className="img-fluid" alt=""/></figure></li>
                                        <li><div className="img-coun">12k</div></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <section>
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-xl-6 col-lg-7 col-md-10 text-center">
                        <div className="sec-heading center">
                            <h2>Featured Jobs</h2>
                            <p>At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores</p>
                        </div>
                    </div>
                </div>
                <FeatureJob/>
            </div>
        </section>
        <HireBox/>

        <section className="pb-4">
            <div className="container">
                <div className="row align-items-center justify-content-between">
                    <div className="col-xl-5 col-lg-5 col-md-12 col-12">
                        <div className="side-thumber-wrap">
                            <div className="side-effect"></div>
                            <div className="side-thumber-img">
                                <figure><img src='/img/side-1.png' className="img-fluid" alt=""/></figure>
                            </div>
                        </div>
                    </div>
                    
                    <div className="col-xl-5 col-lg-6 col-md-12 col-12">
                        <div className="choose-us-head">
                            <div className="choose-us-wriops mb-2"><span className="fw-medium label-light-warning px-3 py-2 rounded">Advanced Features</span></div>
                            <div className="choose-title">
                                <h2 className="lh-base">Trusted & Popular<br/>Job Portal</h2>
                                <p>At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores</p>
                            </div>
                            <div className="jobstock-icon-box-list mt-4">
                                <ul>
                                    {aboutData.map((item,index)=>( 
                                        <li key={index}>
                                            <div className="vib-list-wrap21">
                                                <div className="vib-list-icon">
                                                    <i className="fa-solid fa-check"></i>
                                                </div>
                                                <div className="vib-list-caption">
                                                    <h5>{item.title}</h5>
                                                    <p>{item.desc}</p>
                                                </div>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <div className="clearfix"></div>

        <section className="pt-0">
            <div className="container">
                <div className="row align-items-center justify-content-between">
                    <div className="col-xl-6 col-lg-6 col-md-12 col-12">
                        <div className="p-lg-5 p-md-0 pt-md-5">
                            <div className="mb-4 mb-sm-7">
                                <span className="fw-medium label-light-success px-3 py-2 rounded">Our Showcase</span>
                                <h2 className="mt-2 lh-base">Best Job Search platform<br/>Experience for you</h2>
                                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                            </div>

                            <div className="features-groupss my-4">
                                <ul className="row gx-3 gy-4 p-0">
                                    <li className="fw-medium col-xl-6 col-lg-6 col-6"><span className="square--30 circle d-inline-flex align-items-center justify-content-center text-success bg-light-success me-2"><i className="fa-solid fa-check"></i></span>Corporate Business jobs</li>
                                    <li className="fw-medium col-xl-6 col-lg-6 col-6"><span className="square--30 circle d-inline-flex align-items-center justify-content-center text-success bg-light-success me-2"><i className="fa-solid fa-check"></i></span>Company Showcase</li>
                                    <li className="fw-medium col-xl-6 col-lg-6 col-6"><span className="square--30 circle d-inline-flex align-items-center justify-content-center text-success bg-light-success me-2"><i className="fa-solid fa-check"></i></span>Creative Services</li>
                                    <li className="fw-medium col-xl-6 col-lg-6 col-6"><span className="square--30 circle d-inline-flex align-items-center justify-content-center text-success bg-light-success me-2"><i className="fa-solid fa-check"></i></span>Easy To Upload Resume</li>
                                    <li className="fw-medium col-xl-6 col-lg-6 col-6"><span className="square--30 circle d-inline-flex align-items-center justify-content-center text-success bg-light-success me-2"><i className="fa-solid fa-check"></i></span>Online E-commerce</li>
                                    <li className="fw-medium col-xl-6 col-lg-6 col-6"><span className="square--30 circle d-inline-flex align-items-center justify-content-center text-success bg-light-success me-2"><i className="fa-solid fa-check"></i></span>Hire Expert Candidates</li>
                                </ul>
                            </div>
                        
                            <div className="row">
                                <div className="col-sm-12 col-md-12 col-lg-6">
                                    <Link className="btn btn-main fw-medium px-4" href="#">Explore More Jobs</Link>
                                </div>
                            </div>
                        </div>
                    
                    </div>
                    
                    <div className="col-xl-5 col-lg-5 col-md-12 col-12">
                        <div className="side-thumber-wrap">
                            <div className="side-effect"></div>
                            <div className="side-thumber-img">
                                <figure><img src='/img/side-2.png' className="img-fluid" alt=""/></figure>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <div className="clearfix"></div>

        <CtaOne/>

        <section>
            <div className="container">
                <PricingOne/>
            </div>
        </section>

        <section className="pb-0 bg-cover" style={{backgroundColor:'#01333f', backgroundImage:`url('/img/footer-bg-dark.png')`, backgroundRepeat:'no-repeat'}}>
            <div className="container">
                <div className="row justify-content-between">
                    <div className="col-xl-4 col-lg-6 col-md-12 col-sm-12 order-2">
                        <div className="position-relative">
                            <div className="footlio-img mt-5 mt-lg-0"><img src='/img/mean.png' width={350} className="img-fluid" alt=""/></div>
                        </div>
                    </div>
                    
                    <div className="col-xl-7 col-lg-6 col-md-12 col-sm-12 align-self-center order-1">
                        <div className="footlio-caalaction-caption">
                            <div className="footlio-caalaction-text">
                                <span className="text-main bg-white rounded py-1 px-3">Get Your Job</span>
                                <h2 className="text-light mt-3 mb-4 lh-base">Get your dream jobs just by<br/>uploading your CV</h2>
                                <p className="text-light fs-6 opacity-75">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
                            </div>
                            <div className="footlio-caalaction-link mt-4">
                                <Link href="/upload-cv" className="btn btn-main fw-medium px-4"><i className="fa-solid fa-cloud-arrow-up me-2"></i>Upload CV</Link>
                            </div>
                        </div>
                    </div>
                    
                </div>
                
            </div>		
        </section>

        <FooterLight/>

        <ScrollToTop/>

        <div className={`modal fade `} id="exampleModal" tabIndex={-1} aria-labelledby="exampleModalLabel" aria-hidden="true" style={{backgroundColor:'#0000007d'}}>
            <div className="modal-dialog modal-dialog-centered filter-popup">
                <div className="modal-content">
                    <span className="mod-close" data-bs-dismiss="modal"><i className="fas fa-close"></i></span>
                    <div className="modal-header">
                        <h4 className="modal-header-sub-title text-dark">Start Your Filter</h4>
                    </div>
                    <div className="modal-body p-0">
                        <div className="filter-content">
                            <div className="full-tabs-group">
                                <div className="single-tabs-group">
                                    <div className="single-tabs-group-header text-dark h6"><span>Job Match Score</span></div>
                                    
                                    <div className="single-tabs-group-content">
                                        <div className="d-flex flex-wrap">
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="msix"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="msix">6.0</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="msixfive"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="msixfive">6.5</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="mseven"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="mseven">7.0</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="msevenfive"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="msevenfive">7.5</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="meight"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="meight">8.0</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="meightfive"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="meightfive">8.5</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="mnine"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="mnine">9.0</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="mninefive"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="mninefive">9.5</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="mten"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="mten">10</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="single-tabs-group">
                                    <div className="single-tabs-group-header text-dark h6"><span>Job Value Score</span></div>
                                    
                                    <div className="single-tabs-group-content">
                                        <div className="d-flex flex-wrap">
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="vsix"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="vsix">6.0</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="vsixfive"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="vsixfive">6.5</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="vseven"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="vseven">7.0</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="vsevenfive"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="vsevenfive">7.5</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="veight"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="veight">8.0</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="veightfive"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="veightfive">8.5</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="vnine"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="vnine">9.0</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="vninefive"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="vninefive">9.5</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="vten"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="vten">10</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="single-tabs-group">
                                    <div className="single-tabs-group-header text-dark h6"><span>Place Of Work</span></div>
                                    
                                    <div className="single-tabs-group-content">
                                        <div className="d-flex flex-wrap">
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="anywhere"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="anywhere">Anywhere</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="onsite"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="onsite">On Site</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="remote"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="remote">Fully Remote</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="single-tabs-group">
                                    <div className="single-tabs-group-header text-dark h6"><span>Type Of Contract</span></div>
                                    
                                    <div className="single-tabs-group-content">
                                        <div className="d-flex flex-wrap">
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="employee1"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="employee1">Employee</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="frelancers1"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="frelancers1">Freelancer</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="contractor1"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="contractor1">Contractor</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="internship1"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="internship1">Internship</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="single-tabs-group">
                                    <div className="single-tabs-group-header text-dark h6"><span>Type Of Employment</span></div>
                                    
                                    <div className="single-tabs-group-content">
                                        <div className="d-flex flex-wrap">
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="fulltime"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="fulltime">Full Time</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="parttime"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="parttime">Part Time</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="freelance2"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="freelance2">Freelance</label>
                                            </div>
                                            <div className="sing-btn-groups">
                                                <input type="checkbox" className="btn-check" id="internship2"/>
                                                <label className="btn btn-md btn-outline-main font--bold rounded-5" htmlFor="internship2">Internship</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="single-tabs-group">
                                    <div className="single-tabs-group-header text-dark h6"><span>Radius In Miles</span></div>
                                    
                                    <div className="single-tabs-group-content">
                                        <RangeSlider/>
                                    </div>
                                </div>
                                
                                <div className="single-tabs-group">
                                    <div className="single-tabs-group-header text-dark h6"><span>Explore Top Categories</span></div>
                                    
                                    <div className="single-tabs-group-content">
                                        <ul className="row p-0 m-0">
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-1" className="form-check-input" name="s-1" type="checkbox"/>
                                                    <label htmlFor="s-1" className="form-check-label">IT Computers</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-2" className="form-check-input" name="s-2" type="checkbox"/>
                                                    <label htmlFor="s-2" className="form-check-label">Web Design</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-3" className="form-check-input" name="s-3" type="checkbox"/>
                                                    <label htmlFor="s-3" className="form-check-label">Web development</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-4" className="form-check-input" name="s-4" type="checkbox"/>
                                                    <label htmlFor="s-4" className="form-check-label">SEO Services</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-5" className="form-check-input" name="s-5" type="checkbox"/>
                                                    <label htmlFor="s-5" className="form-check-label">Financial Service</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-6" className="form-check-input" name="s-6" type="checkbox"/>
                                                    <label htmlFor="s-6" className="form-check-label">Art, Design, Media</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-7" className="form-check-input" name="s-7" type="checkbox"/>
                                                    <label htmlFor="s-7" className="form-check-label">Coach & Education</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-8" className="form-check-input" name="s-8" type="checkbox"/>
                                                    <label htmlFor="s-8" className="form-check-label">Apps Developements</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-9" className="form-check-input" name="s-9" type="checkbox"/>
                                                    <label htmlFor="s-9" className="form-check-label">IOS Development</label>
                                                </div>
                                            </li>
                                            <li className="col-lg-6 col-md-6 p-0">
                                                <div className="form-check form-check-inline">
                                                    <input id="s-10" className="form-check-input" name="s-10" type="checkbox"/>
                                                    <label htmlFor="s-10" className="form-check-label">Android Development</label>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                
                                <div className="single-tabs-group">
                                    <div className="single-tabs-group-header text-dark h6"><span>Keywords</span></div>
                                    
                                    <div className="single-tabs-group-content">
                                        <div className="form-group">
                                            <input type="text" className="form-control" placeholder="Design, Java, Python, WordPress etc..."/>
                                        </div>
                                    </div>
                                </div>
                                
                            </div>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <div className="filt-buttons-updates">
                            <button type="button" className="btn btn-dark">Clear Filter</button>
                            <button type="button" className="btn btn-main">Search</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </>
  )
}
