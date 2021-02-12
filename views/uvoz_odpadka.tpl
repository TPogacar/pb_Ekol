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
														<dt> Teža [kg]:
														</dt>
														<dt> <input type="int" name="teza" id="teza" value="{{rezervirano_mesto['teza']['vrednost']}}" placeholder="{{rezervirano_mesto['teza']['ime']}}" class="primary"/> <br>
														</dt>
														<dt> Povzročitelj:
														</dt>
														<dt><input type="text" name="povzrocitelj" id="povzrocitelj" value="{{rezervirano_mesto['povzrocitelj']['vrednost']}}" placeholder="{{rezervirano_mesto['povzrocitelj']['ime']}}" /> 
														</dt>
														<dt> Datum uvoza:
														</dt>
														<dt> <input type="date" name="datum_uvoza" id="datum_uvoza" value="{{rezervirano_mesto['datum_uvoza']['vrednost']}}" placeholder="{{rezervirano_mesto['datum_uvoza']['ime']}}" class="primary"/>
														</dt>
														<dt> Klasifikacijska številka:
														</dt>
														<dt> <input type="text" name="klasifikacijska_stevilka" id="klasifikacijska_stevilka" value="{{rezervirano_mesto['klasifikacijska_stevilka']['vrednost']}}" placeholder="{{rezervirano_mesto['klasifikacijska_stevilka']['ime']}}" class="primary"/>
														</dt>
														<dt> Skladišče:
														</dt>
														<dt> <select name="skladisce" id="skladisce" class="primary">
														<option value={{rezervirano_mesto['skladisce']['vrednost']}}>- {{rezervirano_mesto['skladisce']['ime']}} -</option>
														% from model import Skladisce
														% for id, ime in Skladisce.skladisce():
															<option value={{id}}>{{ime}}</option>
														% end
														</select>
														</dt>
														<dt> Opomba uvoza:
														</dt>
														<dt> <select name="opomba_uvoza" id="opomba_uvoza" />
														<option value={{rezervirano_mesto['opomba_uvoza']['vrednost']}}>- {{rezervirano_mesto['opomba_uvoza']['ime']}} -</option>
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