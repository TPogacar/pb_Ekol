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
									<h2>Uvoz odpadka</h2>

									<p>Za uvoz odpadka izpolnite spodnji obrazec. Ne pozabite, 
									da so za uspešen uvoz odpadka nekateri podatki zahtevani (tj. teža, datum uvoza, klasifikacijska številka, skladišče morajo biti v ustrezni obliki).</p>

									<h4>Podatki o odpadku:</h4>

								<!-- Podatki o odpadku -->
									<form method="POST" action="/podatki_o_odpadku", name="podatki_o_odpadku_odvoz">
										<div class="row gtr-uniform">
											<div>
												
												<div class="col-3 col-12-small">
													<dl class="actions">
														
														<dt> <input type="int" name="teza" id="teza" value="" placeholder="Teža [kg]" class="primary"/> <br>
														</dt>
														<dt><input type="text" name="povzrocitelj" id="povzrocitelj" value="" placeholder="Povzročitelj" /> 
														</dt>
														<dt> <input type="date" name="datum_uvoza" id="datum_uvoza" value="" placeholder="Datum uvoza" class="primary"/>
														</dt>
														<dt> <input type="text" name="klasifikacijska_stevilka" id="klasifikacijska_stevilka" value="" placeholder="Klasifikacijska številka" class="primary"/>
														</dt>
														<dt> <select name="skladisce" id="skladisce" class="primary">
														<option value="">- Skladišče -</option>
														% from model import Skladisce
														% for id, ime in Skladisce.skladisce():
															<option value={{id}}>{{ime}}</option>
														% end
														</select>
														</dt>
														<dt> <select name="opomba_uvoza" id="opomba_uvoza" />
														<option value="">- Opomba -</option>
														% from model import Opomba
														% for id, ime in Opomba.opomba():
															<option value={{id}}>{{ime}}</option>
														% end
														
														</select>			
														</dt>
														<dt><input type="submit" value="Uvozi" class="primary" onclick="if (!confirm('Ali res želite uvoziti odpadek?')) return false;;"/><dt>
														
													</dl>
													</div>
												</ul>
											</div>
										</div>
									</form>


							</div>
						</div>
					</div>
				</div>
			</section>