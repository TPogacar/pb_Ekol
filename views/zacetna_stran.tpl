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
									<h2>Dobrodošli v skladišču!</h2>

									<p>V skladišču podjetja Ekol je mogoče opravljati različne dejavnosti.</p>

									<h4>Kaj želite narediti danes?</h4>



								<!-- IZBIRA DEJAVNOSTI -->

									<form method="POST" action="/izbira_dejavnosti" name="izbira_dejavnosti")>
										<div class="row gtr-uniform">

											<div>
												<div class="col-12">
													<ul class="actions">
													<li><select name="dejavnost" id="dejavnost">
														<option value="">- Izberi -</option>
														<option value="uvoz">Uvoz odpadka</option>
														<option value="izvoz">Izvoz odpadka</option>
														<option value="pregled">Pregled skladiščenih odpadkov</option>
													</select>
													</li>

													<li><input type="submit" value="Pojdi" class="primary" /></li>
												</ul>
											</div>
											</div>

											</div>
									</form>

							</div>
						</div>
					</div>
				</div>
			</section>
