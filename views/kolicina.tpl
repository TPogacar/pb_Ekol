<!--
	spletna stran za uvoz odpadka
-->

% rebase('osnova.tpl', opozorilo=opozorilo)
		
			<section id="main" class="wrapper">
				<div class="inner">
					<div class="content">

					<!-- Elements -->
						<div class="row">
							<div>

								<!-- Text -->
									<h2>Količina posameznih odpadkov</h2>

									<p>Na tem mestu lahko za posamezno skladišče izpišete skupno težo ter število kosov posameznega odpadka
                                    (glede na klasifikacijsko št.). Izpišejo se samo za klasifikacijske številke, ki so v izbranem skladišču.
									Če ne izberete nobenega skladišča, se izpiše za vsa skladišča.</p>

									<h4>Izbira skladišča:</h4>

								    <!-- Izira skladišča -->
									<form method="POST" action="/izpis_kolicina", name="izpis_kolicina">
										<div class="row gtr-uniform">
											<div>
												
												<div class="col-3 col-12-small">
													<dl class="actions">

														<dt> <select name="skladisce" id="skladisce" class="primary">
														<option value="">- Skladišče -</option>
														% from model import Skladisce
														% for id, ime in Skladisce.skladisce():
															<option value={{id}}>{{ime}}</option>
														% end
														</select>
														</dt>
														
														<dt><input type="submit" value="Izpiši" class="primary" /><dt>
														
													</dl>
												</div>
												
											</div>
										</div>
									</form>


							</div>
						</div>
					</div>
				</div>
			</section>