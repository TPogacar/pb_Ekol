<!--
	spletna stran za izvoz odpadka
-->

% rebase('osnova.tpl', opozorilo=opozorilo)
		
			<section id="main" class="wrapper">
				<div class="inner">
					<div class="content">

					<!-- Elements -->
						<div class="row">
							<div>

								<!-- Text -->
									<h2>Izvoz odpadka</h2>

									<p>Odpadke lahko bodisi odstranite, bodisi predelate. V vsakem primeru morate trenutni
									skladiščeni odpadek odstraniti. Za uspešno odstranitev odpadka morate poleg podatkov o
									odpadku (tj. id odpadka) nujno podati ustrezen datum izvedbe dejanja.</p>

									
									<!-- Podatki o odpadku -->
									<form method="POST" action="/podatki_o_odpadku_izvoz", name="podatki_o_odpadku_izvoz">
										<div class="row gtr-uniform">
											<div>
												
												<div class="col-3 col-12-small">
													<dl class="actions">
														<h4>Podatki o odpadku:</h4>
														<dt> <input type="int" name="id" id="id" value="" placeholder="id odpadka" class="primary"/> <br>
														</dt>
														<h4>Podatki o odstranjevanju:</h4>
														<dt> <input type="date" name="datum_izvoza" id="datum_izvoza" value="" placeholder="Datum izvoza" class="primary"/>
														</dt>
														<dt><input type="text" name="prejemnik" id="prejemnik" value="" placeholder="Prejemnik" /> 
														</dt>
														<dt> <select name="opomba_izvoza" id="opomba_izvoza" />
														<option value="">- Opomba -</option>
														% from model import Opomba
														% for id, ime in Opomba.opomba():
															<option value={{id}}>{{ime}}</option>
														% end
														</select>			
														</dt>
														<dt><input type="submit" value="Odstrani" class="primary" onclick="if (!confirm('Ali res želite izvoziti odpadek?')) return false;;"/><dt>
														
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