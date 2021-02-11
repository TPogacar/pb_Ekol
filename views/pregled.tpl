<!--
	zacetna stran spletnega vmesnika
-->

% rebase('osnova.tpl', opozorilo=opozorilo)
		
			<section id="main" class="wrapper">
				<div class="inner">
					<div class="content">

					<!-- Elements -->
						<div class="row">
							<div>

								<!-- Text -->
									<h2>Pregled skladiščenih odpadkov</h2>

									<p>Ker potrebujete pregled nad skladiščenimi odpadki, si lahko na tem mestu ogledate,
                                    kakšno je stanje v skladiščih podjetja Ekol.</p>

									

								<!-- IZBIRA DEJAVNOSTI -->

									<form method="POST" action="/filtriraj" name="filtriraj")>
										<div class="row gtr-uniform">

											<div>
											<!-- izbira dejavnosti -->
											<h4>Kaj vas zanima danes?</h4>

												<div class="col-12">
													<dl class="actions">
														<dt><select name="pregled" id="pregled">
															<option value="">- Izberi -</option>
															<option value="kolicina">Količina posameznih odpadkov</option>
															<option value="nekateri">Vsi odpadki</option>
															<option value="cas">Vsi v nekem časovnem intervalu</option>
                                                    	    <option value="zadnji">Zadnji izvoz</option>
															</select>
														</dt>													
														
														<dt><input type="submit" value="Pojdi" class="primary" /><dt>
																										
												</div>
											</div>

										</div>
									</form>



							</div>
						</div>
					</div>
				</div>
			</section>